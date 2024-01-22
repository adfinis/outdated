import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';

export default class DependencyIndexController extends Controller {
  queryParams = ['name', 'provider'];

  @tracked name = null;
  @tracked provider;

  @tracked model;

  get providers() {
    return ['PIP', 'NPM'];
  }

  get filteredDependencies() {
    let dependencies = this.model;
    if (this.name) {
      dependencies = dependencies.filter((d) =>
        d.name.toLowerCase().includes(this.name.toLowerCase()),
      );
    }
    if (this.provider) {
      dependencies = dependencies.filter((d) => d.provider === this.provider);
    }
    return dependencies;
  }
}
