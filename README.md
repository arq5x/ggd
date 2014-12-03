GGD: Get Genomics Datasets
==========================

This is just a sandbox to demonstrate, explore, and vet some ideas I have for developing a better system for curating relevant genomics datasets (mainly annotations) for reproducible research. I am exploring the use of existing tools such as [dat](http://dat-data.com/) and [conda](http://conda.pydata.org/docs/) for a long term solution. In the interim, this is a place to test ideas and seek feedback.

Note: recipes for datasets retrieved from https://github.com/arq5x/ggd-recipes

Examples
========

Get CpG islands for human build 37 from UCSC 

	$ python ggd.py install ucsc.human.b37.cpg
	searcing for recipe: ucsc.human.b37.cpg
	found recipe: ucsc.human.b37.cpg
	installed ucsc.human.b37.cpg as ucsc.human.b37.cpg

Get CpG islands for human build 38 from UCSC and rename file

	$ python ggd.py install ucsc.human.b38.cpg -o cpg.b38.bed
	searcing for recipe: ucsc.human.b38.cpg
	found recipe: ucsc.human.b38.cpg
	installed ucsc.human.b38.cpg as cpg.b38.bed

Get Clinvar for human build 37 from NCBI

    $ python ggd.py install ncbi.human.b37.clinvar
    searcing for recipe: ncbi.human.b37.clinvar
    found recipe: ncbi.human.b37.clinvar
    installed ncbi.human.b37.clinvar as ncbi.human.b37.clinvar

Try to install a recipe that doesn't exist (nearly everything)

	$ python ggd.py install ucsc.human.b38.dbsnp
	searcing for recipe: ucsc.human.b38.dbsnp
	could not find recipe: ucsc.human.b38.dbsnp
	exiting.
