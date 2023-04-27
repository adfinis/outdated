import Component from '@glimmer/component';

export default class ProjectCompactComponent extends Component {
  get icon() {
    const stateIconDict = {
      OUTDATED: 'bolt',
      WARNING: 'warning',
      'UP-TO-DATE': 'check',
      UNDEFINED: 'info',
    };
    return stateIconDict[this.args.project.status];
  }
  get version() {
    return this.args.project.versionedDependencies.slice()[0];
  }
}
