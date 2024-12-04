FROM ubuntu:latest

RUN apt-get update && apt-get install -y vim python3 python3-pip iputils-ping

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

CMD ["bash"]