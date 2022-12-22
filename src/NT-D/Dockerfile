# base image
FROM pytorch/torchserve-nightly:latest
MAINTAINER Hermes Chen

# install dependencies
RUN pip3 install numpy pandas seaborn lightning tensorboard torch-model-archiver-nightly torch-workflow-archiver-nightly
RUN pip3 install -U --pre torch torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# copy model and related files
COPY production.pt /home/model-server/
COPY handler.py /home/model-server/

# create mar file
WORKDIR /home/model-server/
RUN torch-model-archiver --model-name 'NT-D' --version 1.0  --serialized-file production.pt --handler handler.py

# run Torchserve upon running the container
CMD ["torchserve",
     "--start",
     "--models-store",
     "model-server"]
