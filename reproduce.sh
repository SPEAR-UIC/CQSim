# Build the docker image
echo "Building Image..."
docker build -t cqsimplus:latest .

directory="reproduced_results"
echo "Creating output directory $directory..."
if [ -d "$directory" ]; then
  echo "Directory '$directory' exists. Deleting..."
  rm -rf "$directory" 
fi
echo "Creating directory '$directory'..."
mkdir "$directory"


# Run the docker image and wait for output to be produced under folder reproduced_results
echo "Starting container..."
docker run -v ./$directory:/$directory cqsimplus:latest

