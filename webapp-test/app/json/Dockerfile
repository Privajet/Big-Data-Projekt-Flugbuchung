FROM node:slim

WORKDIR /app

ADD package.json /app/package.json
RUN npm install

ADD index.js /app/index.js

EXPOSE 8080
CMD node index.js