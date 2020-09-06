cd docker/local-jupyter
./build-docker-image.sh
cd ../..

docker run -it --rm                 \
       -p 8888:8888                 \
       -v ${PWD}:/home/jovyan/work  \
       local-jupyter