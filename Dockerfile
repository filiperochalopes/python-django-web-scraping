FROM node:14.14.0 as build_stage

RUN mkdir -p /app
WORKDIR /app
COPY frontend/package.json .
COPY frontend/.env.development .env
RUN yarn
COPY frontend .
RUN yarn build

FROM nginx:1.16.0-alpine

COPY --from=build_stage /app/build /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]