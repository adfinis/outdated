import Component from '@glimmer/component';

export default class ProjectCompactComponent extends Component {
  get icon() {
    let { state } = this.args;
    switch (state) {
      case 'outdated':
        return 'bolt';
      case 'warning':
        return state;
      case 'up-to-date':
        return 'check';
      default:
        console.log(
          'app/components/project-compact/component.js invalid state!'
        );
        return 'invalid state!!!';
    }
  }
}
