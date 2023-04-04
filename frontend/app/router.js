import EmberRouter from '@ember/routing/router';
import config from 'outdated/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

// eslint-disable-next-line array-callback-return
Router.map(function () {
  this.route('projects', { path: '/' }, function () {
    this.route('project-detailed', { path: 'projects/:project_id' });
    this.route('create-new', { path: 'projects/add' });
  });
});
