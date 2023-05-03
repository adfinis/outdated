FROM node:lts-slim as build


EXPOSE 4200 

WORKDIR /ember

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

CMD ["yarn", "start"]

FROM nginx:alpine

COPY --from=build /ember/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf