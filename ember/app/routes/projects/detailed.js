import Route from '@ember/routing/route';
import { service } from '@ember/service';
export default class ProjectDetailedRoute extends Route {
  @service store;
  model(params) {
    return this.store.findRecord('project', params.project_id, {
      include:
        'sources,sources.versions,sources.versions.release-version,sources.versions.release-version.dependency,sources.maintainers,sources.maintainers.user',
    });
  }
}
