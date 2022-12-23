torch-model-archiver -f --model-name 'NT-D' --version 1.0 --serialized-file=docker_image_src/production.pt --handler=docker_image_src/handler.py
torchserve --start --ncs --ts-config=docker_image_src/ts_config --model-store=. --models NT-D=NT-D.mar
