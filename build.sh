set -e
for r in `ls -d ggd-recipes/*/*`; do
	output=$(conda build $r)
	echo $output | grep -Po "(anaconda upload .+)" | sed -e "s/anaconda upload/anaconda upload -u ggd/"
done
