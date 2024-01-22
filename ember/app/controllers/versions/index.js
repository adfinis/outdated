import Controller from '@ember/controller';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';
import { uniq } from 'lodash';

export default class VersionIndexController extends Controller {
  queryParams = ['status', 'dependency', 'version'];

  @tracked status;
  @tracked dependency;
  @tracked version;

  @tracked model;

  @action
  dependencyChanged(value) {
    this.dependency = value?.id;
  }

  get statuses() {
    return ['OUTDATED', 'WARNING', 'UP-TO-DATE', 'UNDEFINED'];
  }

  get dependencies() {
    return uniq(this.model.map((v) => v.releaseVersion.dependency));
  }

  get selectedDependency() {
    return this.dependencies.find((d) => d.id === this.dependency);
  }

  get filteredVersions() {
    let versions = this.model;
    if (this.status) {
      versions = versions.filter((d) => d.status === this.status);
    }
    if (this.selectedDependency) {
      versions = versions.filter(
        (v) => v.releaseVersion.dependency.id === this.dependency,
      );
    }
    if (this.version) {
      versions = versions.filter((v) => v.version.startsWith(this.version));
    }
    return versions;
  }
}
