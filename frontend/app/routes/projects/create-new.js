import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsCreateNewRoute extends Route {
  @service store;
  model() {
    this.store.findAll('dependency');
    this.store.findAll('dependencyVersion');
  }
}
