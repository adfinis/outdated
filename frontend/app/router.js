import EmberRouter from '@ember/routing/router';
import config from 'outdated/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('projects', { path: '/' });
  this.route('project-detailed', { path: 'projects/:id' });
  this.route('create');
});
