set -e
for d in hg38 hg19 hg38-noalt GRCh37; do
	for recipe in ../cloudbiolinux/ggd-recipes/$d/*.yaml; do
		python ggd-2-conda.py --author bcbio $recipe Homo_sapiens $d
	done
done
d=mm10
for recipe in ../cloudbiolinux/ggd-recipes/$d/*.yaml; do
	python ggd-2-conda.py --author bcbio $recipe Mus_musculus $d
done
d=canFam3
for recipe in ../cloudbiolinux/ggd-recipes/$d/*.yaml; do
	python ggd-2-conda.py --author bcbio $recipe Canis_familiaris $d
done
