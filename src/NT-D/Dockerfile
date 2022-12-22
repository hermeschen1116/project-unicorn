# base image
FROM pytorch/torchserve:latest
MAINTAINER Hermes Chen

# save config
USER root
RUN printf "\nservice_envelope=json" >> /home/model-server/config.properties
USER model-server

# install dependencies
RUN pip3 install -U --no-warn-script-location pip wheel setuptools && \
    pip3 install -U --no-warn-script-location numpy pandas seaborn lightning torch-model-archiver-nightly torch-workflow-archiver-nightly && \
    pip3 install -U --no-warn-script-location --pre torch torchaudio torchtext torchvision--extra-index-url https://download.pytorch.org/whl/nightly/cpu

COPY handler.py production.pt /home/model-server/
WORKDIR /home/model-server/
RUN mkdir model-store && \
	torch-model-archiver \
    --model-name NT-D \
    --version 1.0 \
    --serialized-file production.pt \
    --handler handler.py \
    --export-path model_store

EXPOSE 8080
CMD ["torchserve", "--start", "--ncs", "--ts-config=/home/model-server/config.properties", "--model-store", "home/model-server/model-store"]
