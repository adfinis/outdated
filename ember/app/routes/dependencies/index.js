import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class DependencyIndexRoute extends Route {
  @service store;

  async model() {
    await this.store.findAll('project', {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
    });
    return await this.store.peekAll('dependency');
  }
}
