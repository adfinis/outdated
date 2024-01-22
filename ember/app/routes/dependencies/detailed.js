import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class DependencyDetailedRoute extends Route {
  @service store;

  async model({ dependency_id }) {
    await this.store.query('project', {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
      filter: {
        dependency: dependency_id,
      },
    });
    return await this.store.peekRecord('dependency', dependency_id);
  }
}
