module.exports = {
  settings: {
    'import/internal-regex': '^outdated/',
  },
  extends: ['@adfinis/eslint-config/ember-app'],
  overrides: [
    {
      files: ['**/*.{js,ts}'],
      rules: {
        'ember/no-replace-test-comments': 'error',
      },
    },
    {
      files: ['**/*.gjs'],
      parser: 'ember-eslint-parser',
      plugins: ['ember'],
      extends: ['plugin:ember/recommended-gjs'],
    },
    {
      files: ['tests/**/*.{js,ts,gjs,gts}'],
      rules: {
        'ember/no-replace-test-comments': 'error',
      },
    },
  ],
};
