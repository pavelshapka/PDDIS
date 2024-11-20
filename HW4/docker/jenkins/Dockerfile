FROM jenkins/jenkins:lts
USER root

RUN apt-get update && apt-get install -y vim python3 python3-pip python3.11-venv bash maven ansible
COPY requirements.txt .
RUN /bin/bash -c "pip install --no-cache-dir --break-system-packages -r requirements.txt"

CMD ["/usr/local/bin/jenkins.sh"]