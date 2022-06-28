FROM ubuntu:20.04

# Setup python and java and base system
ENV DEBIAN_FRONTEND noninteractive
ENV LANG=en_US.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en supervisor

RUN pip3 install --upgrade pip requests
RUN pip3 install python-docx docxtpl tika numpy pandas
RUN pip3 install -U setuptools wheel
RUN pip3 install -U spacy

RUN mkdir ./app
COPY . ./app
WORKDIR ./app



# verify permissions set
RUN ls -lah /usr/lib/python3/dist-packages/

# put the requirements file into the container
COPY requirements.txt ./requirements.txt

# install the requirements in the container
RUN pip install -r requirements.txt \
  && chmod 777 /usr/lib/python3/dist-packages/*

# verify permissions set
RUN ls -lah /usr/lib/python3/dist-packages/

EXPOSE 8501

CMD sudo streamlit run app.py --server.port $PORT