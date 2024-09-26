FROM ubuntu:latest

RUN apt-get update && apt-get install -y poppler-utils

WORKDIR /data

CMD ["/bin/bash"]
