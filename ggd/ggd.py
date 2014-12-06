#!/usr/bin/env python

import argparse
import os
import requests
import shutil
import subprocess
import sys
import tempfile
import urllib2
import yaml


recipe_urls = {
  "core": "https://raw.githubusercontent.com/arq5x/ggd-recipes/master/",
  "api": "https://api.github.com/repos/arq5x/ggd-recipes/git/trees/master?recursive=1"
  }

def get_install_path(config_path):
    if config_path is None:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'config.yml')
    with open(config_path, 'r') as f:
        config = yaml.load(f.read())
    return config['path']['root']

def _get_recipe(args, url):
  """
  http://stackoverflow.com/questions/16694907/\
  how-to-download-large-file-in-python-with-requests-py
  """
  print >> sys.stderr, "searching for recipe: " + args.recipe

  # hanndle core URL and http:// and ftp:// based cookbooks
  if args.cookbook is None or "file://" not in args.cookbook:
    r = requests.get(url, stream=True)
    if r.status_code == 200:
      print >> sys.stderr, "found recipe: " + args.recipe
      return r.text
    else:
      print >> sys.stderr, "could not find recipe: " + args.recipe
      return None
  #responses library doesn't support file:// requests
  else:
    r = urllib2.urlopen(url)
    if r.getcode() is None:
      print >> sys.stderr, "found recipe: " + args.recipe
      return r.read()
    else:
      print >> sys.stderr, "could not find recipe: " + args.recipe
      return None



def _run_recipe(args, recipe):
  """
  Execute the contents of a YAML-structured recipe.
  """

  if args.region is None:
    # bash, etc.
    recipe_version = recipe['attributes']['version']
    recipe_type = recipe['recipe']['full']['recipe_type']
    # specific commnads to execute recipe.
    recipe_cmds = recipe['recipe']['full']['recipe_cmds']
    # the output file names for the recipe.
    recipe_outfiles = recipe['recipe']['full']['recipe_outfiles']
  else:
    if 'region' in recipe['recipe']:
      # bash, etc.
      recipe_type = recipe['recipe']['region']['recipe_type']
      # specific commnads to execute recipe.
      recipe_cmds = recipe['recipe']['region']['recipe_cmds']
      # the output file names for the recipe.
      recipe_outfiles = recipe['recipe']['region']['recipe_outfiles']
    else:
      print >> sys.stderr, "region queries not supported for " + args.recipe

  tempdir = tempfile.mkdtemp()
  install_path = get_install_path(args.config)
  for idx, cmd in enumerate(recipe_cmds):
    out_file = os.path.join(tempdir, recipe_outfiles[idx])
    f = open(out_file, 'w')
    if recipe_type == 'bash':
      if args.region is not None:
        cmd += ' ' + args.region
      destination = os.path.join(install_path, args.recipe, str(recipe_version))
      ret = subprocess.call(cmd, stdout=f, shell=True)
      if ret: # return non-zero if failure
          print >> sys.stderr, "failure installing " + args.recipe
    else:
      print >> sys.stderr, "recipe_type not yet supported"
    f.close()
    if not os.path.exists(destination):
        os.makedirs(destination)
    shutil.move(out_file, destination)
  shutil.rmtree(tempdir)
  return True


def install(parser, args):
  """
  Install a dataset based on a GGD recipe
  """
  recipe = args.recipe

  if args.cookbook is None:
    recipe_url = recipe_urls['core'] + recipe + '.yaml'
  else:
    recipe_url = args.cookbook + recipe + '.yaml'

  # get the raw YAML string contents of the recipe
  recipe = _get_recipe(args, recipe_url)

  if recipe is not None:
    # convert YAML to a dictionary
    recipe_dict = yaml.load(recipe)
    if _run_recipe(args, recipe_dict):
      print >> sys.stderr, "installed " + args.recipe
    else:
      print >> sys.stderr, "failure installing " + args.recipe
  else:
    print >> sys.stderr, "exiting."


def list(parser, args):
  """
  List all available datasets
  """
  request = requests.get(recipe_urls['api'])
  tree = request.json()['tree']
  for branch in tree:
    if ".yaml" in branch["path"]:
      print branch['path'].rstrip('.yaml')


def search(parser, args):
    """
    Search for a recipe
    """
    recipe = args.recipe
    request = requests.get(recipe_urls['api'])
    tree = request.json()['tree']
    matches = [branch['path'] for branch in tree if recipe in branch['path'] and ".yaml" in branch["path"]]
    if matches:
        print "Available recipes:"
        print "\n".join(match.rstrip('.yaml') for match in matches)
    else:
        print >> sys.stderr, "No recipes available for {}".format(recipe)


def main():

  # create the top-level parser
  parser = argparse.ArgumentParser(prog='ggd')
  parser.add_argument("-v", "--version", help="Installed ggd version",
                      action="version",
                      version="alpha")
  subparsers = parser.add_subparsers(title='[sub-commands]', dest='command')

  # parser for install tool
  parser_install = subparsers.add_parser('install',
    help='Install a dataset based on a recipe')
  parser_install.add_argument('recipe',
    metavar='STRING',
    help='The GGD recipe to use.')
  parser_install.add_argument('--region',
    dest='region',
    metavar='STRING',
    required=False,
    help='A genomic region to extract. E.g., chr1:100-200')
  parser_install.add_argument('--cookbook',
    dest='cookbook',
    metavar='STRING',
    required=False,
    help='A URL to an alternative collection of '
    'recipes that follow the GGD ontology')
  parser_install.add_argument('--config',
    dest='config',
    metavar='STRING',
    required=False,
    help='Absolute location to config file')
  parser_install.set_defaults(func=install)

  # parser for list tool
  parser_list = subparsers.add_parser('list',
    help='List available recipes')
  parser_list.set_defaults(func=list)

  parser_search = subparsers.add_parser('search',
    help='Search available recipes')
  parser_search.add_argument('recipe',
    metavar='STRING',
    help='The GGD recipe to search.')
  parser_search.set_defaults(func=search)

  # parse the args and call the selected function
  args = parser.parse_args()

  try:
    args.func(parser, args)
  except IOError, e:
       if e.errno != 32:  # ignore SIGPIPE
           raise

if __name__ == "__main__":
    main()
