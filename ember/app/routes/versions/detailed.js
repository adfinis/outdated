import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class DependencyDetailedRoute extends Route {
  @service store;

  async model({ version_id }) {
    await this.store.query('project', {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency,maintainers,maintainers.user',
      filter: {
        version: version_id,
      },
    });
    return await this.store.peekRecord('version', version_id);
  }
}
