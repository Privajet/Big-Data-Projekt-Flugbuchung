FROM postgres 
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB ccmgmtdb
EXPOSE 5000
COPY dump_ccmgmt_db.sql /docker-entrypoint-initdb.d/
COPY startup.sh ./
COPY waitforit.sh ./
RUN mkdir -p /ccmgmt_data
RUN apt-get update && apt-get install -y python3 python3-pip
COPY ccmgmt_data/ /ccmgmt_data
WORKDIR /ccmgmt_data
RUN pip3 install -r requirements.txt
WORKDIR /
CMD ["./startup.sh"]  

 