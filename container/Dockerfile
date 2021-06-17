FROM python:3

LABEL maintainer="Gakuto Furuya"

RUN apt update \
  && apt install -y texlive-full \
  xpdf

COPY ./requirements.txt requirements.txt
COPY ./tex.py /usr/local/bin
COPY ./texpdf.py /usr/local/bin
COPY ./tex-template /tex-template

RUN pip install -r requirements.txt \
  && chmod +x /usr/local/bin/tex.py \
  && chmod +x /usr/local/bin/texpdf.py
