FROM danlynn/ember-cli:4.11.0 as build

COPY package.json yarn.lock /myapp/

RUN yarn install

COPY . /myapp/

RUN yarn build

FROM nginx:alpine

COPY --from=build /myapp/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf