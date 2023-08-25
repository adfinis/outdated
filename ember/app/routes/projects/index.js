import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProjectsRoute extends Route {
  @service store;

  beforeModel() {
    const unsavedProject = this.store
      .peekAll('project')
      .find((project) => project.isNew);
    unsavedProject?.destroyRecord();
  }

  model() {
    return this.store.findAll('project', {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency,maintainers,maintainers.user',
    });
  }
}
