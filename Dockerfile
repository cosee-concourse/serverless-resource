FROM node:7-alpine

RUN mkdir -p /aws && \
    apk -Uuv add python3 && \
    rm /var/cache/apk/*

COPY opt /opt

RUN pip3 install -r /opt/requirements.txt

# SET Serverless Version like
# docker build --build-arg serverlessVersion=1.6.1
ARG serverlessVersion

RUN npm install --loglevel error -g serverless@$serverlessVersion

CMD serverless