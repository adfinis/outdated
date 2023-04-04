import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsCreateNewRoute extends Route {
  @service store;
  beforeModel() {
    this.store.findAll('dependency');
    this.store.findAll('dependencyVersion');
  }

  deactivate() {
    this.store.unloadAll('project');
  }
}
