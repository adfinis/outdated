import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsDetailedEdit extends Route {
  @service store;
  beforeModel() {
    this.store.findAll('user');
    this.store.findAll('maintainer');
  }
}
