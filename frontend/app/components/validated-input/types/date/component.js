import { action } from '@ember/object';
import Component from '@glimmer/component';
export default class DateInputComponent extends Component {
  @action
  onUpdate(value) {
    this.args.update(value[0]);
  }
}
