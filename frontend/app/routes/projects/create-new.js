import Route from '@ember/routing/route';
import { service } from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { hash } from 'rsvp';

class Model {
  @tracked saved = false;

  save() {
    this.saved = true;
  }
}

export default class ProjectsCreateNewRoute extends Route {
  @service store;
  model() {
    return hash({
      model: new Model(),
      dependencies: this.store.findAll('dependency'),
      dependencyVersions: this.store.findAll('dependencyVersion'),
      project: this.store.findRecord('project', 1, {
        include: 'dependencyVersions,dependencyVersions.dependency',
      }),
    });
  }
}
