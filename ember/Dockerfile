FROM danlynn/ember-cli:4.11.0 as build

# install yarn dependencies
COPY package.json yarn.lock ./


# copy the rest of the app

COPY . /myapp/

RUN yarn install

RUN yarn build --environment=production

FROM nginx:alpine

COPY --from=build /myapp/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf