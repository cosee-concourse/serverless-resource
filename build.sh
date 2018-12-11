docker build --pull \
        -t $CONTAINER_IMAGE_NAME:latest \
        -t $CONTAINER_IMAGE_NAME:1.34.1 \
        -t $CONTAINER_IMAGE_NAME:1.34 \
        --build-arg serverlessVersion=1.34.1 .

docker build \
        -t $CONTAINER_IMAGE_NAME:1.32.0 \
        -t $CONTAINER_IMAGE_NAME:1.32 \
        --build-arg serverlessVersion=1.32.0 .

docker build \
        -t $CONTAINER_IMAGE_NAME:1.31.0 \
        -t $CONTAINER_IMAGE_NAME:1.31 \
        --build-arg serverlessVersion=1.31.0 .
