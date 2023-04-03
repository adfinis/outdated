import { action } from '@ember/object';
import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsCreateNewRoute extends Route {
  @service store;
  model() {
    this.store.findAll('dependency');
    this.store.findAll('dependencyVersion');
  }
  @action
  async deactivate() {
    await this.store.unloadRecord(
      // eslint-disable-next-line ember/no-controller-access-in-routes
      this.store.findRecord('project', this.controller.project.id)
    );
  }
}
