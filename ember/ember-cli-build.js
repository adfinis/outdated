'use strict';

const BrotliPlugin = require('brotli-webpack-plugin');
const EmberApp = require('ember-cli/lib/broccoli/ember-app');
module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    // Add options here
  });

  const { Webpack } = require('@embroider/webpack');
  return require('@embroider/compat').compatBuild(app, Webpack, {
    skipBabel: [
      {
        package: 'qunit',
      },
    ],

    packagerOptions: {
      webpackConfig: {
        plugins:
          app.env === 'production'
            ? [
                new BrotliPlugin({
                  asset: '[path].br[query]',
                  test: /\.(js|css|html|svg)$/,
                  minRatio: 0.8,
                }),
              ]
            : [],
      },
    },
  });
};
