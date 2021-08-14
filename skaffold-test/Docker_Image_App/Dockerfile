FROM python:3.7.3-stretch
# this is required for hot reload
ENV FLASK_DEBUG=1
ENV FLASK_APP hello.py

COPY ./hello.py /app/hello.py
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]