FROM jupyter/all-spark-notebook:spark-3.2.0

WORKDIR /home/dev/notebook

COPY . .

RUN pip install -r requirements.txt

USER root

EXPOSE 8888
