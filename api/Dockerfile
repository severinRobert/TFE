FROM alpine:3.17

RUN apk update
RUN apk upgrade
RUN apk add python3

RUN python3 -m ensurepip
COPY . /api
WORKDIR /api
RUN pip3 install -r requirements.txt
RUN python3 main.py


CMD ["tail", "-f", "/dev/null"]