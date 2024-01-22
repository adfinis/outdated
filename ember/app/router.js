import EmberRouter from '@ember/routing/router';

import config from 'outdated/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

const resetNamespace = true;

// eslint-disable-next-line array-callback-return
Router.map(function () {
  this.route('login');
  this.route('protected', { path: '/' }, function () {
    this.route('index', { resetNamespace, path: '/' }, function () {
      this.route('dependencies', { resetNamespace }, function () {
        this.route('detailed', { path: '/:dependency_id' });
      });
      this.route('versions', { resetNamespace }, function () {
        this.route('detailed', { path: '/:version_id' });
      });
      this.route('projects', { resetNamespace, path: '/' }, function () {
        this.route('detailed', { path: 'projects/:project_id' }, function () {
          this.route('edit');
        });
        this.route('add', { path: 'projects/add' });
      });
    });
    this.route('not-found', { resetNamespace, path: '/*path' });
  });
});
