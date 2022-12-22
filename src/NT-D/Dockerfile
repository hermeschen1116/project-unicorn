# base image
FROM pytorch/torchserve:latest
MAINTAINER Hermes Chen

VOLUME [ "/home/model-server/" ]
WORKDIR /home/

# copy model and related files
COPY production.pt handler.py /home/model-server/

# save config
USER root
RUN printf "\nservice_envelope=json" >> /home/model-server/config.properties
USER model-server

# install dependencies
RUN pip3 install -U --no-warn-script-location pip wheel setuptools && \
    pip3 install -U --no-warn-script-location numpy pandas seaborn lightning torch-model-archiver torch-workflow-archiver && \
    pip3 install -U --no-warn-script-location --pre torch torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# create mar file
RUN torch-model-archiver --model-name 'NT-D' --version 1.0 \
    --serialized-file=/home/model-server/production.pt \
    --handler=/home/model-server/handler.py \
    --export-path=/home/model-server/model-store

EXPOSE 8080
CMD ["torchserve", "--start", "--ncs", "--ts-config=/home/model-server/config.properties", "--model-store", "home/model-server/model-store"]
