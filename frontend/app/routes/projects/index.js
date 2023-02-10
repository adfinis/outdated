import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsProjectsRoute extends Route {
  @service store;
  model() {
    return this.store.findAll('project', {
      include: 'dependencyVersions,dependencyVersions.dependency',
    });
  }
}
