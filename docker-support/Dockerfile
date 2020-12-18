FROM public.registry.u-hopper.com/python:3.8



RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wenet-common-models-requirements.txt .
RUN pip install --no-cache-dir -r wenet-common-models-requirements.txt

WORKDIR /scripts

COPY run.sh .


ADD src/ /scripts/
ADD documentation/ /documentation/

ENV DOCUMENTATION_PATH /documentation

ADD test/ /scripts/tests/
COPY run_tests.sh .
COPY test.sh .



ENV PYTHONPATH /scripts

CMD ["./run.sh"]
