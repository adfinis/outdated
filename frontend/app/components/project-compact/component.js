import Component from '@glimmer/component';

export default class ProjectCompactComponent extends Component {
  get icon() {
    let { project } = this.args;
    switch (project.status) {
      case 'OUTDATED':
        return 'bolt';
      case 'WARNING':
        return 'warning';
      case 'UP-TO-DATE':
        return 'check';
      default:
        return 'invalid';
    }
  }
  get version() {
    let { project } = this.args;
    return project.dependencyVersions.toArray()[0];
  }
}
