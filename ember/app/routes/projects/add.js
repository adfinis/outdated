import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsAddRoute extends Route {
  @service store;
  beforeModel() {
    this.store.findAll('dependency');
    this.store.findAll('releaseVersion');
    this.store.findAll('version');
    this.store.findAll('user');
    this.store.findAll('maintainer');
  }
}
