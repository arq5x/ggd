#!/usr/bin/env python

import os
import sys
import argparse
import requests
import urllib2
import subprocess

recipe_urls = {
  "core": "https://raw.githubusercontent.com/arq5x/ggd-recipes/master/",
  }


def _download_file(args, url):
  """
  http://stackoverflow.com/questions/16694907/\
  how-to-download-large-file-in-python-with-requests-py
  """
  local_filename = url.split('/')[-1]
  print >> sys.stderr, "searcing for recipe: " + args.recipe
  r = requests.get(url, stream=True)
  if r.status_code == 200:
    print >> sys.stderr, "found recipe: " + args.recipe
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename
  else:
    print >> sys.stderr, "could not find recipe: " + args.recipe
    return None


def _run_recipe(recipe, outfile):
  f = open(outfile, 'w')
  ret = subprocess.call(['bash', recipe], stdout=f)
  return ret


def install(parser, args):
  """
  Install a dataset based on a GGD recipe
  """
  # replace "." in recipe with slashes
  recipe = args.recipe.replace('.', '/')

  recipe_url = recipe_urls['core'] + recipe + '.sh'
  recipe_file = _download_file(args, recipe_url)

  if recipe_file is not None:
    outfile = args.outfile 
    if outfile is None:
      outfile = args.recipe

    failure = _run_recipe(recipe_file, outfile)
    if not failure:
      print >> sys.stderr, "installed " + args.recipe + " as " + outfile
    else:
      print >> sys.stderr, "failure installing " + args.recipe
    #os.remove(recipe_file)
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
  parser_install.add_argument('-o',
    dest='outfile',
    metavar='STRING',
    required=False,
    help='The name of the output file.')
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