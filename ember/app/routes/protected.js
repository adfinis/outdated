import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class ProtectedRoute extends Route {
  @service session;

  async beforeModel(transition) {
    await this.session.requireAuthentication(transition, 'login');
  }
}
