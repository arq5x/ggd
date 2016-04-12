import yaml
import sys
import os
import gzip


if sys.version_info[0] < 3:
    import urllib
    urlopen = urllib.urlopen
else:
    from urllib.request import urlopen


def xopen(path):
    if path.startswith(("https://", "http://")):
        return urlopen(path)
    if path.endswith(".gz"):
        return gzip.open(path)
    return open(path)

def mkdir(path):
    print("making new directory: {0}".format(new_dir))
    try:
        os.makedirs(new_dir)
    except OSError:
        return

def convert_yaml(old, source_urls, build_reqs=None, run_reqs=None):
    build_reqs #= build_reqs or ['TODO']
    run_reqs #= run_reqs or ['TODO']

    new = {'package': dict(name=old['attributes'].pop('name'),
                           version=old['attributes'].pop('version'))}
    if len(old['attributes']) == 0:
        del old['attributes']

    new['source'] =  [{"url": s, "fn": s.split("/", 1)[-1]} for s in source_urls]
    new['requirements'] = {'build': build_reqs, 'run': run_reqs}

    new['build'] = {'binary_relocation': False,
                    'detect_binary_files_with_prefix': False}


    return new




if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--strict", default=False, action="store_true", help="add 'set -e' to bash scripts")
    p.add_argument("--use-build", default=False, action="store_true", help="write recipe to build.sh, default is to use pre-link.sh")
    p.add_argument("--source-url", default=[], action="append", help="source file(s) to use. May be specified many times.")
    p.add_argument("yaml")

    a = p.parse_args()
    assert os.path.exists(a.yaml) or a.yaml.startswith("http")

    new_dir = os.path.basename(a.yaml).rsplit(".", 1)[0]
    mkdir(new_dir)

    old = yaml.load(xopen(a.yaml))

    recipe = old['recipe']['full']['recipe_cmds']

    script = "build" if a.use_build else "pre-link"
    with open("{new_dir}/{script}.sh".format(new_dir=new_dir, script=script), "w") as fh:
        fh.write("#!/bin/bash\n")
        fh.write("set -eo pipefail\n\n")
        fh.write("# converted from: {0}\n\n".format(a.yaml))
        fh.write("\n\n".join(recipe))


    new = convert_yaml(old, a.source_url)
    yaml.dump(new, open("{new_dir}/meta.yaml".format(new_dir=new_dir), "w"),
              default_flow_style=False)
