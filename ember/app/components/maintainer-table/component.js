import Component from '@glimmer/component';

export default class MaintainerTableComponent extends Component {
  get maintainers() {
    // prevent sort-by helper from using deprecated .toArray
    return this.args.maintainers?.slice();
  }
}
