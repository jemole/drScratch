FROM python:2-onbuild

LABEL maintainer="Cristian David Chushig Muzo <cdavid.chushig@gmail.com>"

USER root

RUN apt-get -qq update && DEBIAN_FRONTEND=noninteractive apt-get -y \
    install sudo xvfb \
    git wget python-virtualenv python-numpy python-scipy netpbm \
    python-pyqt5 ghostscript libffi-dev libjpeg-turbo-progs \
    python-dev python-setuptools \
    python3-dev cmake  \
    libtiff5-dev libjpeg-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
    python-tk python3-tk \
    libharfbuzz-dev libfribidi-dev && apt-get clean

RUN git clone https://github.com/python-pillow/Pillow.git && cd Pillow/depends \
    && ./install_openjpeg.sh && ./install_raqm.sh

RUN mkdir /code/
WORKDIR /code/
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# Latest version of Hairball framework
RUN git clone https://github.com/jemole/hairball.git /code/hairball \
        && cd /code/hairball && pip install .

ADD . /code/

# COPY ./docker-entrypoint.sh /
# ENTRYPOINT ["/docker-entrypoint.sh"]
