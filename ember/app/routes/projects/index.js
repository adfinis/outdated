import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsRoute extends Route {
  @service store;

  model() {
    return this.store.findAll('project', {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
    });
  }
}
