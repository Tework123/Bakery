FROM node:20-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
#COPY frontend/bakery-app/package.json yarn.lock ./
#COPY frontend/bakery-app/package-lock.json ./
#COPY frontend/bakery-app/package.json ./
#
#COPY frontend/bakery-app/src ./src
#COPY frontend/bakery-app/public ./public

COPY frontend/bakery-app ./
RUN npm install
RUN npm run build



FROM nginx:1.25-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
COPY deployment/nginx/nginx.conf /etc/nginx/conf.d/default.conf