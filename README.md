GGD: Get Genomics Data
==========================

This is just a sandbox to demonstrate, explore, and vet some ideas I have for developing a better system for curating relevant genomics datasets (mainly annotations) for reproducible research. I am exploring the use of existing tools such as [dat](http://dat-data.com/) and [conda](http://conda.pydata.org/docs/) for a long term solution. In the interim, this is a place to test ideas and seek feedback.

The recipes for datasets retrieved from https://github.com/arq5x/ggd-recipes

The recipes follow an ontology. For example, one could use GGD to install CpG islands from UCSC for Human build 38.  The command would be:

	# Recipe hierarchy: source/species/genomebuild/name
	ggd install ucsc/human/b38/cpg

In this case, the recipe would live at:

	https://github.com/arq5x/ggd-recipes/ucsc/human/b38/cpg.yaml

Overview of the GDD design (long term vision):

![overview](https://raw.githubusercontent.com/arq5x/ggd/master/_images/overview.png)


Installation
============

    git clone https://github.com/arq5x/ggd
    cd ggd
    sudo python setup.py install


Example usage
=============

GGD uses a configuration file ('config.yaml') to control where the datasets that it installs are placed on your file system. By default, this will be $HOME/ggd_data. 

Get CpG islands for human build 37 from UCSC 

	$ ggd install ucsc/human/b37/cpg
    searching for recipe: ucsc/human/b37/cpg
    found recipe: ucsc/human/b37/cpg
    installed ucsc/human/b37/cpg

    $ ls -1 $HOME/ggd_data
    ucsc.human.b37.cpg

If you would the datasets to be placed somewhere else, one can change the path that is used with the `setpath` tool.

	$ ggd setpath --path ~/mydata/


Now get CpG islands for human build 38 from UCSC. Note that the location of the dataset has changed to ~/mydata/

	$ ggd install ucsc/human/b38/cpg
    searching for recipe: ucsc/human/b38/cpg
    found recipe: ucsc/human/b38/cpg
    installed ucsc/human/b38/cpg

    $ ls -1 ~/mydata/
    ucsc.human.b38.cpg

Get Clinvar VCF and Tabix index for human build 37 from NCBI

    $ ggd install ncbi/human/b37/clinvar
    searching for recipe: ncbi/human/b37/clinvar
    found recipe: ncbi/human/b37/clinvar
    installed ncbi/human/b37/clinvar

    $ ls -1 ~/mydata/
    ucsc.human.b38.cpg
	clinvar-latest.vcf.gz
	clinvar-latest.vcf.gz.tbi

Get a specific genomic region from Clinvar VCF via Tabix for human build 37 from NCBI

	$ ggd install ncbi.human.b37.clinvar \
	         --region 22:20000000-30000000

	$ ls -1 ~/mydata/
    ucsc.human.b38.cpg
	clinvar-latest.region.vcf
	clinvar-latest.vcf/gz
	clinvar-latest.vcf.gz.tbi

Get ExAC VCF and Tabix index for human build 37 from ExAC website (slower)

	$ ggd install misc/human/b37/exac
    searching for recipe: misc/human/b37/exac
    found recipe: misc/human/b37/exac
    installed misc/human/b37/exac

    $ ls -1 ~/mydata/
    ucsc.human.b38.cpg
	clinvar-latest.region.vcf
	clinvar-latest.vcf.gz
	clinvar-latest.vcf.gz.tbi
    ExAC.r0.2.sites.vep.vcf.gz
    ExAC.r0.2.sites.vep.vcf.gz.tbi

Try to install a recipe that doesn't exist (nearly everything)

	$ ggd install ucsc/human/b38/dbsnp
    searching for recipe: ucsc/human/b38/dbsnp
    could not find recipe: ucsc/human/b38/dbsnp
    exiting.

Search for recipes
	
	$ ggd search cpg
	Available recipes:
	ucsc/human/b37/cpg
	ucsc/human/b38/cpg

List all recipes (currently very few)

	$ ggd list
	misc/human/b37/exac
	ncbi/human/b37/clinvar
	ucsc/human/b37/alus
	ucsc/human/b37/cpg
	ucsc/human/b38/cpg
	...


Dependencies
============
We will try to minimize these as much as possible.

1. Mysql
2. Curl
3. pyyaml
4. Python 2.7
5. Tabix
