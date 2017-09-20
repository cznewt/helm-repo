FROM python:2.7-alpine

COPY . /videoviz
RUN pip install /videoviz

WORKDIR /videoviz

ENTRYPOINT ["./videoviz.py"]
