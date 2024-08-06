FROM python:3.10.14

COPY demo_dockerfile/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY demo_dockerfile/src /app/
WORKDIR /app/

CMD ["python", "./main.py"]
