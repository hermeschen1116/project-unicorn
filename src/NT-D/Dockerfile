# base image
# use FROM pytorch/torchserve:latest-gpu for GPU support
FROM pytorch/torchserve:latest

# install dependencies
RUN pip3 install numpy pandas seaborn lightning tensorboard torch-model-archiver-nightly torch-workflow-archiver-nightly torchserve-nightly
RUN pip3 install -U --pre torch torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu

# copy model archive
COPY production.pt /home/model-server/model-store/

# create mar file
WORKDIR /home/model-server/model-store/
RUN torch-model-archiver --model-name 'NT-D' --version 1.0  --serialized-file production.pt --handler <default_handler>

# run Torchserve upon running the container
CMD ["torchserve",
     "--start",
     "--models my_model=BERTweetSentimentAnalysis.mar",
     "--ts-config /home/model-server/config.properties"]
