DEPENDANCY=$(which convert)
DIR=$(~/Pictures)
IMAGE_URL="https://rustyquill.com/wp-content/uploads/2022/01/Newall-Alexander.jpg"
FILENAME=$(echo $IMAGE_URL | awk -F '/' '{print $8}')

# ensure dependancies are installed
if [ -z DEPENDANCY ]; 
then sudo apt-get update && sudo apt-get install imagemagick wget
fi

# Download image
wget $IMAGE_URL

# ensure ~/Pictures directory exists and convert image 
mkdir -p $DIR
convert $FILENAME -crop 240x240+106+17 $DIR/alexanderjnewall.jpg
