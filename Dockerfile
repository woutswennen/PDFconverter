FROM ubuntu:20.04

# Setup python and java and base system
ENV DEBIAN_FRONTEND noninteractive
ENV LANG=en_US.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en supervisor && \
    apt install python3.8-venv \

EXPOSE 9000
EXPOSE 80

RUN python3 -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir ./app
COPY . ./app

RUN mkdir ~/.streamlit
COPY config.toml ~/.streamlit/config.toml
COPY credentials.toml ~/.streamlit/credentials.toml

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN pip3 install --upgrade pip requests
RUN pip3 install python-docx tika numpy pandas
RUN pip3 install -U setuptools wheel
RUN pip3 install -U spacy
RUN python3 -m spacy download en_core_web_lg

WORKDIR ./app

#ENTRYPOINT ["streamlit", "run"]
#CMD ["app.py"]

CMD streamlit run app.py --server.port 9000