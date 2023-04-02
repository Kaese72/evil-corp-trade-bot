# syntax=docker/dockerfile:1
FROM python:latest
COPY . .
RUN pip install -r requirements.txt; python setup.py install
CMD ["python", "-m", "evilbot"]