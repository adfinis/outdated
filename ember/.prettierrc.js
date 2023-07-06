'use strict';

module.exports = {
  plugins: ['prettier-plugin-ember-template-tag'],
  singleQuote: true,
  overrides: [
    {
      files: '*.{js,ts,gjs,gts}',
    },
  ],
};
