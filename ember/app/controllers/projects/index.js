import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';

export default class DependencyIndexController extends Controller {
  queryParams = ['status', 'name'];

  @tracked name;
  @tracked status;

  @tracked model;

  get statuses() {
    return ['OUTDATED', 'WARNING', 'UP-TO-DATE', 'UNDEFINED'];
  }

  get filteredProjects() {
    let projects = this.model;
    if (this.name) {
      projects = projects.filter((p) =>
        p.name.toLowerCase().includes(this.name.toLowerCase()),
      );
    }
    if (this.status) {
      projects = projects.filter((p) => p.status === this.status);
    }
    return projects;
  }
}
