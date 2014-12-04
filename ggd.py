#!/usr/bin/env python

import os
import sys
import argparse
import requests
import urllib2
import subprocess
import yaml

recipe_urls = {
  "core": "https://raw.githubusercontent.com/arq5x/ggd-recipes/master/",
  }


def _get_recipe(args, url):
  """
  http://stackoverflow.com/questions/16694907/\
  how-to-download-large-file-in-python-with-requests-py
  """
  local_filename = url.split('/')[-1]
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
  Execute the contents of a recipe.
  """

  if args.region is None:
    # bash, etc.
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

  for idx, cmd in enumerate(recipe_cmds):
    f = open(recipe_outfiles[idx], 'w')
    if recipe_type == 'bash':
      if args.region is not None:
        cmd += ' ' + args.region
      ret = subprocess.call(cmd, stdout=f, shell=True)
      if ret: # return non-zero if failure
        print >> sys.stderr, "failure installing " + args.recipe
    else:
      print >> sys.stderr, "recipe_type not yet supported"
    f.close()

  return True


def install(parser, args):
  """
  Install a dataset based on a GGD recipe
  """
  # replace "." in recipe with slashes
  recipe = args.recipe.replace('.', '/')

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
  List a available datasets
  """
  pass


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
  parser_install.set_defaults(func=install)

  # parser for list tool
  parser_list = subparsers.add_parser('list', 
    help='List available recipes')
  parser_list.set_defaults(func=list)

  # parse the args and call the selected function
  args = parser.parse_args()

  try:
    args.func(parser, args)
  except IOError, e:
       if e.errno != 32:  # ignore SIGPIPE
           raise

if __name__ == "__main__":
    main()