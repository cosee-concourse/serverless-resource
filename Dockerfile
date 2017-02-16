FROM node:7-alpine

RUN mkdir -p /aws && \
    apk -Uuv add groff less python3 && \
    pip3 install awscli jsonschema && \
    rm /var/cache/apk/*

# SET Serverless Version like
# docker build --build-arg serverlessVersion=1.6.1
ARG serverlessVersion

RUN npm install -g serverless@$serverlessVersion

COPY opt /opt

CMD serverless