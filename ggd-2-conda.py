import yaml
import sys
import os
import gzip
import re


if sys.version_info[0] < 3:
    import urllib
    urlopen = urllib.urlopen
else:
    from urllib.request import urlopen
    unicode = str


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

def convert_yaml(old, species, build, build_reqs=None, run_reqs=None):
    build_reqs = build_reqs or []
    run_reqs = run_reqs or []

    new = {'package': dict(name="{0}-{1}".format(build, old['attributes'].pop('name')),
                           version=str(old['attributes'].pop('version')).replace("-", "."))}
    new['package']['name'] = new['package']['name'].lower()
    if len(old['attributes']) == 0:
        del old['attributes']

    new['requirements'] = {'build': build_reqs, 'run': run_reqs}

    new['build'] = {'binary_relocation': False,
                    'detect_binary_files_with_prefix': False}
    return new

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--strict", default=False, action="store_true", help="add 'set -e' to bash scripts")
    p.add_argument("--author", type=str, default=None)
    p.add_argument("--use-build", default=False, action="store_true", help="write recipe to build.sh, default is to use pre-link.sh")
    p.add_argument("yaml")
    p.add_argument("species")
    p.add_argument("genome_build")

    a = p.parse_args()
    assert os.path.exists(a.yaml) or a.yaml.startswith("http")
    print(a.yaml)
    try:
        old = yaml.load(xopen(a.yaml))
    except yaml.scanner.ScannerError:
        v = xopen(a.yaml).read().replace("\t", "    ")
        import io
        s = io.StringIO(unicode(v))
        old = yaml.load(s)

    name = old['attributes']['name'].lower()
    new_dir = os.path.join("ggd-recipes", a.species, (a.genome_build + "-" + name).lower())
    mkdir(new_dir)


    recipe = old['recipe']['full']['recipe_cmds']

    new = convert_yaml(old, a.species, a.genome_build)
    work_dir = "$PREFIX/share/ggd/{species}/{genome_build}/{pkg_name}/".format(
            species=a.species, genome_build=a.genome_build, pkg_name=new['package']['name'])

    script = "build" if a.use_build else "pre-link"
    with open("{new_dir}/{script}.sh".format(new_dir=new_dir, script=script), "w") as fh:
        fh.write("#!/bin/bash\n")
        fh.write("set -eo pipefail\n\n")
        fh.write("# converted from: {0}\n\n".format(a.yaml))
        fh.write("mkdir -p {work_dir} && cd {work_dir}\n\n".format(work_dir=work_dir))
        fh.write("\n\n".join(recipe))



    xtra = []
    for line in xopen(a.yaml):
        if line[0] != "#" and line.strip(): break
        xtra.append(line.strip("#"))
    if xtra:
        new['about'] = {'summary': "\n".join(xtra)}
    if a.author:
        new['extra'] = {"authors": a.author}

    with open("{new_dir}/meta.yaml".format(new_dir=new_dir), "w") as yfh:
        yaml.dump(new, yfh, default_flow_style=False)
        yfh.write("# to make a pre-built package, move pre-link.sh to build.sh\n")
        yfh.write("# and add source and fn here\n")
        yfh.write("#source:\n    #url: http://example.com/ex.tgz\n    #fn: ex.tgz\n")
