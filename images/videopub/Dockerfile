FROM python:2.7-jessie

COPY setup.py videopub.py /videopub/
RUN apt-get update && apt-get -y install libopencv-dev python-opencv
RUN pip install /videopub

ENTRYPOINT ["videopub"]
