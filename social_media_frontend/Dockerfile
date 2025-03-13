FROM node:20-alpine

WORKDIR /app

COPY package.json .

RUN npm install --package-lock-only

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]