import Component from '@glimmer/component';

export default class ProjectCompactComponent extends Component {
  get icon() {
    const { project } = this.args;
    const stateIconDict = {
      OUTDATED: 'bolt',
      WARNING: 'warning',
      'UP-TO-DATE': 'check',
      UNDEFINED: 'info',
    };
    return stateIconDict[project.status];
  }
  get version() {
    const { project } = this.args;
    return project.dependencyVersions.slice()[0];
  }
}
