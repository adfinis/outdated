import Component from '@glimmer/component';

export default class DependencyCompactComponent extends Component {
  get color() {
    let { state } = this.args;
    switch (state) {
      case 'outdated':
        return 'danger';
      case 'warning':
        return state;
      case 'up-to-date':
        return 'success';
      default:
        return 'invalid';
    }
  }
}
