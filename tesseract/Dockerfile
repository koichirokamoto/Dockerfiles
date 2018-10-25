FROM ubuntu:18.10

ENV TESSDATA_PREFIX=/tessdata

RUN apt-get update && \
  apt-get install -y tesseract-ocr git

RUN git clone https://github.com/tesseract-ocr/tessdata_best.git $TESSDATA_PREFIX

