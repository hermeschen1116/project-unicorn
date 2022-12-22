# base image
FROM pytorch/torchserve:latest
MAINTAINER Hermes Chen

# copy model and related files
COPY production.pt handler.py /home/model-server/

# install dependencies
RUN pip3 install numpy pandas seaborn lightning tensorboard torch-model-archiver torch-workflow-archiver
RUN pip3 install -U --pre torch torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# save config
USER root
RUN printf "\nservice_envelope=json" >> /home/model-server/config.properties
USER model-server

# create mar file
RUN torch-model-archiver --model-name 'NT-D' --version 1.0 \
    --serialized-file=/home/model-server/production.pt \
    --handler=/home/model-server/handler.py \
    --export-path=/home/model-server/model-store

EXPOSE 8080
CMD ["torchserve", "--start", "--ncs", "--ts-config=/home/model-server/config.properties", "--models-store", "model-server/model-store"]
