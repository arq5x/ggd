GGD. Test

Note: recipes for datasets retrieved from https://github.com/arq5x/ggd-recipes

Examples:

	# get CpG islands for human build 37 from UCSC 
	$ python ggd.py install ucsc.human.b37.cpg
	searcing for recipe: ucsc.human.b37.cpg
	found recipe: ucsc.human.b37.cpg
	installed ucsc.human.b37.cpg as ucsc.human.b37.cpg

	# get CpG islands for human build 38 from UCSC and rename file
	$ python ggd.py install ucsc.human.b38.cpg -o cpg.b38.bed
	searcing for recipe: ucsc.human.b38.cpg
	found recipe: ucsc.human.b38.cpg
	installed ucsc.human.b38.cpg as cpg.b38.bed

	# try to install a recipe that doesn't exist (nearly everything)
	$ python ggd.py install ucsc.human.b38.dbsnp
	searcing for recipe: ucsc.human.b38.dbsnp
	could not find recipe: ucsc.human.b38.dbsnp
	exiting.
