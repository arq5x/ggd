set -e

#rm -f $(conda info --root)/conda-bld/linux-64/*
#rm -f osx-64/*
#for r in `ls -d ggd-recipes/*/*`; do
#	output=$(conda build $r)
#	echo $output | grep -Po "(anaconda upload .+)" | sed -e "s/anaconda upload/anaconda upload -u ggd-alpha/"
#done
#
#for f in $(conda info --root)/conda-bld/linux-64/*.bz2; do
#	if [[ "$(basename $f)" == "repodata.json.bz2" ]]; then
#	   	continue
#   	fi
#	echo $f
#	conda convert -p osx-64 $f
#done
#
for f in $(conda info --root)/conda-bld/linux-64/*.bz2; do
	if [[ "$(basename $f)" == "repodata.json.bz2" ]]; then
	   	continue
   	fi
	anaconda upload --force -u ggd-alpha $f;
done

for f in osx-64/*.bz2; do
	if [[ "$(basename $f)" == "repodata.json.bz2" ]]; then
	   	continue
   	fi
	anaconda upload --force -u ggd-alpha $f;
done
