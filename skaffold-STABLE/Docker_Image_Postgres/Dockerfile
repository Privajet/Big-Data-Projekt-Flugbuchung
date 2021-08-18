FROM postgres 
ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB kranichairline_db
EXPOSE 5002
COPY kranichairline_db.sql /docker-entrypoint-initdb.d/
WORKDIR /


 