import { action } from '@ember/object';
import Component from '@glimmer/component';
export default class SelectComponent extends Component {
  @action
  onUpdate(value) {
    this.args.update(value);
  }
}
