FROM alpine:3.20

RUN apk add --update --no-cache openssh ansible sshpass openrc py3-pip
RUN mkdir -p ~/.ssh

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

CMD ["sh"]