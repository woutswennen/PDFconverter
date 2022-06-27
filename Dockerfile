FROM ubuntu:20.04

# Setup python and java and base system
ENV DEBIAN_FRONTEND noninteractive
ENV LANG=en_US.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en supervisor

RUN pip3 install --upgrade pip requests
RUN pip3 install python-docx tika numpy pandas
RUN pip3 install -U setuptools wheel
RUN pip3 install -U spacy
RUN python -m spacy download en_core_web_lg

RUN mkdir ./app
COPY . ./app
WORKDIR ./app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
