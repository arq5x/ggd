GGD: Get Genomics Datasets
==========================

This is just a sandbox to demonstrate, explore, and vet some ideas I have for developing a better system for curating relevant genomics datasets (mainly annotations) for reproducible research. I am exploring the use of existing tools such as [dat](http://dat-data.com/) and [conda](http://conda.pydata.org/docs/) for a long term solution. In the interim, this is a place to test ideas and seek feedback.

The recipes for datasets retrieved from https://github.com/arq5x/ggd-recipes

The recipes follow an ontology. For example, one could use GGD to install CpG islands from UCSC for Human build 38.  The command would be:

	# source.species.genomebuild.name
	python ggd.py install ucsc.human.b38.cpg

In this case, the recipe would live at:

	https://github.com/arq5x/ggd-recipes/ucsc/human/b38/cpg.yaml


Examples
========

Get CpG islands for human build 37 from UCSC 

	$ python ggd.py install ucsc.human.b37.cpg
    searching for recipe: ucsc.human.b37.cpg
    found recipe: ucsc.human.b37.cpg
    installed ucsc.human.b37.cpg

    $ ls -1
    ucsc.human.b37.cpg

Get CpG islands for human build 38 from UCSC

	$ python ggd.py install ucsc.human.b38.cpg
    searching for recipe: ucsc.human.b38.cpg
    found recipe: ucsc.human.b38.cpg
    installed ucsc.human.b38.cpg

    $ ls -1
    ucsc.human.b37.cpg
    ucsc.human.b38.cpg

Get Clinvar VCF and Tabix index for human build 37 from NCBI

    $ python ggd.py install ncbi.human.b37.clinvar
    searching for recipe: ncbi.human.b37.clinvar
    found recipe: ncbi.human.b37.clinvar
    installed ncbi.human.b37.clinvar

    $ ls -1
    ucsc.human.b37.cpg
    ucsc.human.b38.cpg
	clinvar-latest.vcf.gz
	clinvar-latest.vcf.gz.tbi


Get ExAC VCF and Tabix index for human build 37 from ExAC website (slower)

	$ python ggd.py install misc.human.b37.exac
    searching for recipe: misc.human.b37.exac
    found recipe: misc.human.b37.exac
    installed misc.human.b37.exac

    $ ls -1
    ucsc.human.b37.cpg
    ucsc.human.b38.cpg
	clinvar-latest.vcf.gz
	clinvar-latest.vcf.gz.tbi
    ExAC.r0.2.sites.vep.vcf.gz
    ExAC.r0.2.sites.vep.vcf.gz.tbi

Try to install a recipe that doesn't exist (nearly everything)

	$ python ggd.py install ucsc.human.b38.dbsnp
    searching for recipe: ucsc.human.b38.dbsnp
    could not find recipe: ucsc.human.b38.dbsnp
    exiting.


Dependencies
============
We will try to minimize these as much as possible.

1. Mysql
2. Curl
3. pyyaml
4. Python 2.7
5. Tabix
