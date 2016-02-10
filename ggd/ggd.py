#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import requests
import shutil
import subprocess
import sys
import datetime
import urllib2
import yaml
from string import Template

import utils


recipe_urls = {
  "core": "https://raw.githubusercontent.com/arq5x/ggd-recipes/master/",
  "api": "https://api.github.com/repos/arq5x/ggd-recipes/git/trees/master?recursive=1"
  }


def set_install_path(data_path, config_path):
    """
    Change the path for installing datasets.
    """
    config = utils._get_config_data(config_path)
    # change the data path and update the config file
    config['path']['root'] = data_path
    with open(config_path, 'w') as f:
        f.write(yaml.dump(config, default_flow_style=False))


def register_installed_recipe(args, recipe_dict):
    """
    Add a dataset to the list of installed datasets
    in the config file.
    """
    pass


def _get_recipe(recipe, cookbook=None):
    """
    http://stackoverflow.com/questions/16694907/\
    how-to-download-large-file-in-python-with-requests-py
    """
    sys.stderr.write("searching for recipe: " + recipe + "...")
    url = url_for_recipe(recipe, cookbook)

    # hanndle core URL and http:// and ftp:// based cookbooks
    if cookbook is None or "file://" not in cookbook:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            sys.stderr.write("ok\n")
            return yaml.load(r.text)
        else:
            sys.stderr.write("failed\n")
            return None
    #responses library doesn't support file:// requests
    else:
        r = urllib2.urlopen(url)
        if r.getcode() is None:
            sys.stderr.write("ok\n")
            return yaml.load(r.read())
        else:
            # TODO: set error code
            sys.stderr.write("failed\n")
            return None

def make_deps(deps, install_path, cookbook, overwrite=False):
    # deps looks like: [{'version': 1, 'name': 't2'}, {'version': 1, 'name': 't1'}]
    for dep in deps:
        sys.stderr.write("\ninstalling dependency: {name}:{version}\n"\
                .format(**dep))

        recipe_dict = _get_recipe(dep['name'], cookbook)
        sha1s = utils.get_list(recipe_dict['attributes'], 'sha1')
        ret = make(recipe_dict["recipe"]["make"], dep['name'], dep['version'], install_path,
             cookbook,
             sha1s=sha1s, overwrite=overwrite)
        code = utils.msg_unless(ret == 0, code=ret, msg="error installing dependency: %s" % dep['name'])
        if code != 0:
            sys.exit(code)


def make(recipe, name, version, install_path, cookbook, sha1s=None, overwrite=False):
    # check that we have the software that we need.
    software = utils.get_list(recipe, ('dependencies', 'software'))
    msg = "didn't find required software: %s for %s\n" % (software, name)
    code = utils.msg_unless(utils.check_software_deps(software), code=5, msg=msg)
    if code != 0: return code

    data_deps = utils.get_list(recipe, ("dependencies", "data"))
    make_deps(data_deps, install_path, cookbook, overwrite)


    out_files = []

    # set template variables
    tmpl_vars = dict(GGD_PATH=install_path, version=version,
                     name=name,
                     DATE=datetime.date.today().strftime("%Y-%m-%d"))

    # TODO: data dependencies
    for i, cmd in enumerate(recipe['cmds']):
        if sha1s is None:
            tmpl_vars['sha1'] = ''
        else:
            try:
                tmpl_vars['sha1'] = sha1s[i]
            except IndexError:
                tmpl_vars['sha1'] = ''
                sys.stderr.write("WARNING: no SHA1 provided for recipe %s/%d\n" % (name, i))

        tcmd = Template(cmd).safe_substitute(tmpl_vars)

        out = Template(recipe['outfiles'][i]).safe_substitute(tmpl_vars)
        code = utils.msg_unless(utils.check_outfiles([out], overwrite))
        if code != 0: return code

        out_files.append(out)

        ret = subprocess.check_call(tcmd, shell=True)
        msg = "error processing recipe."
        code = utils.msg_unless(ret == 0, code=ret, msg=msg)
        if code != 0: return code

        code = utils.msg_unless(sha_matches(out, tmpl_vars['sha1'], name), code=4)
        if code != 0: return code

    for out in out_files:
        if os.path.exists(os.path.join(install_path, out)):
            if overwrite:
                os.unlink(os.path.join(install_path, out))
            else:
                code = utils.msg_unless(False, code=1,
                            msg="ERROR: output file %s exists. Use --overwrite if needed" %
                            os.path.join(install_path, out))
                if code != 0: return code
        shutil.move(out, install_path)

    return 0

def _run_recipe(args, recipe):
    """
    Execute the contents of a YAML-structured recipe.
    """
    return make(recipe['recipe']['make'],
                recipe['attributes']['name'],
                recipe['attributes']['version'],
                utils.get_install_path(args),
                args.cookbook,
                sha1s=utils.get_list(recipe['attributes'], 'sha1'),
                overwrite=args.overwrite)

def sha_matches(path, expected_sha, recipe):
    if expected_sha is None or expected_sha == '': return True
    sys.stderr.write("validating dataset SHA1 checksum for %s...\n" % path)
    if not os.path.exists(path):
        sys.stderr.write("ERROR: path not found: %s...\n" % path)
        return False

    obs = utils._get_sha1_checksum(path)
    if obs == expected_sha:
        sys.stderr.write("ok (" + obs + ")\n\n")
        return True
    else:
        sys.stderr.write("ERROR in sha1 check. obs: %s != exp %s\n" % (obs, expected_sha))
        sys.stderr.write("failure installing " + recipe + ".\n")
        sys.stderr.write("perhaps the connection was disrupted? try again?\n")
        return False

def url_for_recipe(recipe, cookbook=None):
    return "{cookbook}{recipe}.yaml".format(cookbook=cookbook or "", recipe=recipe)

def install(args):
    """
    Install a dataset based on a GGD recipe
    """
    recipe = args.recipe
    utils.setup(args)

    # get the raw YAML string contents of the recipe
    recipe_dict = _get_recipe(recipe, args.cookbook)

    if recipe_dict is None:
        sys.stderr.write("recipe not found exiting.\n")
        sys.exit(2)

    ret = _run_recipe(args, recipe_dict)
    if ret == 0:
        # TO DO
        # register_installed_recipe(args, recipe_dict)
        sys.stderr.write("installed " + args.recipe + "\n")
    else:
        sys.stderr.write("failure installing " + args.recipe + "\n")
    sys.exit(ret)


def list_recipes(args):
    """
    List all available datasets
    """
    request = requests.get(recipe_urls['api'])
    tree = request.json()['tree']
    for branch in tree:
        if ".yaml" in branch["path"]:
            print(branch['path'].rstrip('.yaml'))


def search_recipes(args):
    """
    Search for a recipe
    """
    recipe = args.recipe
    request = requests.get(recipe_urls['api'])
    tree = request.json()['tree']
    matches = [branch['path'] for branch in tree if recipe in branch['path'] and ".yaml" in branch["path"]]
    if matches:
        print("Available recipes:")
        print("\n".join(match.rstrip('.yaml') for match in matches))
    else:
        print("No recipes available for {}".format(recipe), file=sys.stderr)


def setpath(args):
    """
    Set the path to use for storing installed datasets
    """
    set_install_path(args.path, args.config)


def main():

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

    parser_install.add_argument('--overwrite',
        action='store_true',
        help='Overwrite existing files with the same name.'
             ' Default is to error if this happens.')

    parser_install.set_defaults(func=install)

    # parser for list tool
    parser_list = subparsers.add_parser('list',
      help='List available recipes')

    parser_list.set_defaults(func=list_recipes)

    # parser for search tool
    parser_search = subparsers.add_parser('search',
      help='Search available recipes')

    parser_search.add_argument('recipe',
      metavar='STRING',
      help='The GGD recipe to search.')
    parser_search.set_defaults(func=search_recipes)

    # parser for setpath tool
    parser_setpath = subparsers.add_parser('setpath',
      help='Set the path to which datasets should be installed.')

    parser_setpath.add_argument('--path',
      dest='path',
      metavar='STRING',
      help='The data path to use.')

    parser_setpath.add_argument('--config',
      dest='config',
      metavar='STRING',
      required=False,
      help='Absolute location to a specific config file')
    parser_setpath.set_defaults(func=setpath)

    # parser for getpath tool
    parser_getpath = subparsers.add_parser('where',
      help='Display the path in which datasets are installed.')

    parser_getpath.add_argument('--config',
      dest='config',
      metavar='STRING',
      required=False,
      help='Absolute location to a specific config file')

    parser_getpath.set_defaults(func=utils.get_install_path)

    # parse the args and call the selected function
    args = parser.parse_args()

    try:
        args.func(args)
    except IOError, e:
        if e.errno != 32:  # ignore SIGPIPE
            raise

if __name__ == "__main__":

    main()
