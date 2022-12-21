FROM nikolaik/python-nodejs:latest
WORKDIR /app
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
RUN pip install --upgrade setuptools pip wheel eel numpy
COPY . .
CMD [ "python3", "app.py" ]
