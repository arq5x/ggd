import os
import sys
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'ggd', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','')
long_description = """
``ggd`` is a toolset for getting genomics datasets'
"""

with open("requirements.txt", "r") as f:
    install_requires = [x.strip() for x in f.readlines()]

setup(
        name="ggd",
        version=version,
        install_requires=install_requires,
        requires = ['python (>=2.7, <3.0)'],
        packages=['ggd',
                  'ggd.scripts'],
        author="Aaron Quinlan",
        description='A toolset for getting genomics datasets',
        long_description=long_description,
        url="",
        package_dir = {'ggd': "ggd"},
        package_data = {'ggd': [], '': ['config.yaml']},
        zip_safe = False,
        include_package_data=True,
        entry_points = {
            'console_scripts' : [
                 'ggd = ggd.ggd:main'
            ],
        },
        scripts = ['ggd/scripts/query_biomart.py'],
        author_email="arq5x@virginia.edu",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Scientific/Engineering :: Bio-Informatics']
    )
