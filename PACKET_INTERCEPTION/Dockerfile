FROM python:3.13.0a1-bookworm
RUN apt update && apt install -y iptables
RUN apt install -y build-essential python3-dev libnfnetlink-dev libnetfilter-queue-dev iproute2 inetutils-ping
WORKDIR /app
COPY . .
# RUN bash setup.sh
RUN pip3 install -r requirements.txt 
# RUN bash ./src/shell/ramdisk.sh
RUN bash ./src/shell/iptables.sh