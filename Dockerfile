FROM ubuntu:xenial
RUN apt-get update -y && apt-get install -y\
    python-pip\
    python-dev\
    build-essential\
    libssl-dev\
    libffi-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && python setup.py install
ENTRYPOINT ["python"]
CMD ["column/api/run.py"]
