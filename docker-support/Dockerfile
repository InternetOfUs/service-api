FROM registry.u-hopper.com:5000/uhopper/utils-py:0.7.2

MAINTAINER Stefano Tavonatti <stefano.tavonatti@u-hopper.com>

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh .

ADD src/ /scripts/

ENV PYTHONPATH /scripts

CMD ["./run.sh"]
