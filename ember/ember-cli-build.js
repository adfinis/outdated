'use strict';

const BrotliPlugin = require('brotli-webpack-plugin');
const EmberApp = require('ember-cli/lib/broccoli/ember-app');
module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    'ember-simple-auth': {
      useSessionSetupMethod: true,
    },
  });

  const { Webpack } = require('@embroider/webpack');
  return require('@embroider/compat').compatBuild(app, Webpack, {
    skipBabel: [
      {
        package: 'qunit',
      },
    ],
    // https://github.com/embroider-build/embroider/issues/1322
    packageRules: [
      {
        package: '@ember-data/store',
        addonModules: {
          '-private.js': {
            dependsOnModules: [],
          },
          '-private/system/core-store.js': {
            dependsOnModules: [],
          },
          '-private/system/model/internal-model.js': {
            dependsOnModules: [],
          },
        },
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
