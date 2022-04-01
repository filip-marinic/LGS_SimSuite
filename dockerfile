FROM registry.esa.int:5020/sepp/jl_base:latest
ENV DEBIAN_FRONTEND noninteractive

COPY ./requirements.txt /tmp/ 
RUN apt-get update \ && pip3 install -r /tmp/requirements.txt

COPY ./*.ipynb /media/notebooks/
