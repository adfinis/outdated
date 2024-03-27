import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class DependencyIndexRoute extends Route {
  @service store;

  async model() {
    await this.store.findAll('project', {
      include:
        'sources,sources.versions,sources.versions.release-version,sources.versions.release-version.dependency',
    });
    return await this.store.peekAll('version');
  }
}
