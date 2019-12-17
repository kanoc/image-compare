FROM python:3.7
MAINTAINER Csaba Szotyori <kanocspam@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/image_compare
RUN mkdir -p /opt/services/images
COPY requirements.txt /opt/services/image_compare/
COPY requirements.in /opt/services/image_compare/
WORKDIR /opt/services/image_compare/
RUN pip install -r requirements.txt
COPY app /opt/services/image_compare/
COPY tasks.py /opt/services/image_compare/
COPY setup.py /opt/services/image_compare/
COPY env_file /opt/services/image_compare/
RUN inv install
EXPOSE 9009

CMD ["python", "/opt/services/image_compare/app/web/server.py"]
