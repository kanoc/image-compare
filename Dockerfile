FROM python:3.7-slim
LABEL MAINTAINER = "Csaba Szotyori <kanocspam@gmail.com>"

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/image_compare && mkdir -p /opt/services/images
COPY app tasks.py setup.py requirements.in requirements.txt /opt/services/image_compare/
WORKDIR /opt/services/image_compare/
RUN pip install -r requirements.txt && inv install

EXPOSE 9009

CMD ["python", "/opt/services/image_compare/app/web/server.py"]
