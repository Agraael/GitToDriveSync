FROM golang:alpine as drive

ARG credentials
ARG ssh_prv_key
ARG ssh_pub_key
ARG port=8080

RUN set -e -u -x \
&& apk add --no-cache --no-progress build-base git \
&& go get -u github.com/odeke-em/drive/drive-gen \
&& drive-gen

RUN apk update && apk add python3 openssh

ADD gitdrive .
ADD $credentials ./credentials.json

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

EXPOSE $port

ENTRYPOINT [ "python3", "-u", "./gitdrive", "auto", "--json", "credentials.json", "--hook", "--link"]
