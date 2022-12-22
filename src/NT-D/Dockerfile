# base image
FROM pytorch/torchserve:latest
MAINTAINER Hermes Chen

COPY handler.py production.pt /home/model-server/

# install dependencies
RUN pip3 install -U --no-warn-script-location numpy pandas seaborn lightning torch-model-archiver torch-workflow-archiver

WORKDIR /home/
RUN torch-model-archiver --model-name 'NT-D' --version 1.0 \
    --serialized-file=/home/model-server/production.pt \
    --handler=/home/model-server/handler.py \
     --export-path=/home/model-server/model-store

CMD ["torchserve", "--start", "--model-store=/home/model-server/model-store", "--models", "NT-D=/home/model-server/model-store/NT-D.mar"]
