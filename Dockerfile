FROM python:3.6
MAINTAINER Hiram <jie.zhang8@luckyair.net>

# install tesseract
RUN apt-get update
RUN apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev
RUN pip install tesserocr

# install google chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0

RUN mkdir /myapp
WORKDIR /myapp
COPY entrypoint.sh /myapp/
COPY requirements.txt /myapp/
COPY run.py /myapp/
COPY cookiespool /myapp/cookiepool/
COPY login /myapp/login/



RUN pip install -r requirements.txt && pip install uwsgi
RUN chmod +x entrypoint.sh

EXPOSE 5000

CMD ["/myapp/entrypoint.sh"]