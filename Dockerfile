FROM node:lts-alpine as build-stage
RUN cd ..
RUN mkdir /frontend
WORKDIR /frontend
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build

FROM ubuntu:20.04 as backend-builder
ENV LANG=en_US.UTF-8
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev supervisor
RUN pip3 install --upgrade pip requests
RUN mkdir /app
COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY --from=build-stage /frontend/dist /app/dist
RUN ls