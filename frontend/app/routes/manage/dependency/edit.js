import Route from '@ember/routing/route';
import { service } from '@ember/service';
export default class DependencyEditRoute extends Route {
  @service store;
  model(params) {
    return this.store.findRecord('dependency', params.dependency_id);
  }
}
