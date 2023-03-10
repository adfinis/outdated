import { action } from '@ember/object';
import { scheduleOnce } from '@ember/runloop';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
export default class FormComponent extends Component {
  @tracked submitted = false;

  constructor(...args) {
    super(...args);

    if (this.args.model && this.args.model.validate) {
      scheduleOnce('actions', this, 'validateModel', this.args.model);
    }
  }

  validateModel(model) {
    model.validate();
  }

  @action
  async submit(e) {
    e.preventDefault();
    this.submitted = true;

    const model = this.args.model;

    await model.validate();
    if (model.get('isInvalid')) {
      // implement logic here
    }
    return false;
  }
}
