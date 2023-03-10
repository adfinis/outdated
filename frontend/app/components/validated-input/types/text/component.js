import { action } from '@ember/object';
import Component from '@glimmer/component';
export default class TextInputComponent extends Component {
  @action
  onUpdate(e) {
    e.preventDefault();

    this.args.update(e.target.value);
  }
}
