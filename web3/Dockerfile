FROM node:21-alpine

WORKDIR /app/web3

COPY . .

RUN npm install

RUN chmod +x entrypoint.sh
RUN chmod +x deploy.sh

CMD ["./entrypoint.sh"]