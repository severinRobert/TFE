FROM alpine:3.17

RUN apk update
RUN apk upgrade
RUN apk add python3

RUN python3 -m ensurepip
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /api
RUN python3 main.py


CMD ["tail", "-f", "/dev/null"]