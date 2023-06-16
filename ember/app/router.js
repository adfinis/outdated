import EmberRouter from '@ember/routing/router';
import config from 'outdated/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

// eslint-disable-next-line array-callback-return
Router.map(function () {
  this.route('login');
  this.route('protected', { path: '/' }, function () {
    this.route('index', { resetNamespace: true, path: '/' }, function () {
      this.route('projects', { resetNamespace: true, path: '/' }, function () {
        this.route('detailed', { path: 'projects/:project_id' }, function () {
          this.route('edit');
        });
        this.route('add', { path: 'projects/add' });
      });
    });
  });
});
