FROM python:2.7-alpine

COPY setup.py videopub.py /videopub/
RUN pip install /videopub

ENTRYPOINT ["videopub"]
