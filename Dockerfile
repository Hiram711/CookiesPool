FROM joyzoursky/python-chromedriver:3.6-selenium
MAINTAINER Hiram <jie.zhang8@luckyair.net>

RUN mkdir /myapp
WORKDIR /myapp
COPY ./* /myapp



# install tesseract
RUN apt-get update
RUN apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install uwsgi

EXPOSE 5000

CMD ["entrypoint.sh"]