# base image
FROM pytorch/torchserve:latest
MAINTAINER Hermes Chen

VOLUME [ "/home/model-server" ]

# install dependencies
RUN pip3 install numpy pandas seaborn lightning tensorboard torch-model-archiver torch-workflow-archiver
RUN pip3 install -U --pre torch torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# copy model and related files
WORKDIR /home/model-server
COPY production.pt /home/model-server
COPY handler.py /home/model-server

# create mar file
RUN torch-model-archiver --model-name 'NT-D' --version 1.0  --serialized-file production.pt --handler handler.py

EXPOSE 8080
CMD ["torchserve", "--start", "--ncs", "--models-store", "model-store"]
