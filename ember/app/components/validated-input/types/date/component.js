import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';

export default class DateInputComponent extends Component {
  @service intl;

  get locale() {
    return this.intl.primaryLocale.split('-')[0];
  }

  @action
  onUpdate(value) {
    this.args.update(value[0]);
  }
}
