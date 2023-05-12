import { service } from '@ember/service';
import OIDCJSONAPIAdapter from 'ember-simple-auth-oidc/adapters/oidc-json-api-adapter';

export default class ApplicationAdapter extends OIDCJSONAPIAdapter {
  @service session;

  namespace = 'api';
  get headers() {
    return { ...this.session.headers, 'Content-Language': 'en-us' };
  }
}
