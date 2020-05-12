FROM python:3.8-alpine

MAINTAINER Stefano Tavonatti <stefano.tavonatti@u-hopper.com>

RUN apk add --update bash

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /scripts

COPY run.sh .

COPY run_tests.sh .

ADD src/ /scripts/
ADD tests/ /scripts/tests/

ENV PYTHONPATH /scripts

CMD ["./run.sh"]
