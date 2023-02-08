import Component from '@glimmer/component';

export default class ProjectCompactComponent extends Component {
  get icon() {
    let { project } = this.args;
    const stateIconDict = {
      OUTDATED: 'bolt',
      WARNING: 'warning',
      'UP-TO-DATE': 'check',
      UNDEFINED: 'info',
    };
    return stateIconDict[project.status];
  }
  get version() {
    let { project } = this.args;
    return project.dependencyVersions.toArray()[0];
  }
}
