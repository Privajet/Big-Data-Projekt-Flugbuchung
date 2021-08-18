FROM busybox 
EXPOSE 5000
COPY startup.sh ./
RUN mkdir -p /app_data
RUN yum -y install wget
RUN apt-get update && apt-get install -y python3 python3-pip
COPY app_data/ /app_data
WORKDIR /app_data
RUN pip3 install -r requirements.txt
WORKDIR /
CMD ["./startup.sh"]  

 