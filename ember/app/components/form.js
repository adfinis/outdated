import { action } from '@ember/object';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { scheduleTask } from 'ember-lifeline';

export default class FormComponent extends Component {
  @tracked loading = false;
  @tracked submitted = false;

  constructor(...args) {
    super(...args);

    if (this.args.model && this.args.model.validate) {
      scheduleTask(this, 'actions', () => this.args.model.validate());
    }
  }

  @action
  async submit(e) {
    e.preventDefault();
    this.submitted = true;
    const model = this.args.model;
    if (!model?.validate) {
      return false;
    }
    await model.validate();
    if (!model.get('isInvalid')) {
      const onSubmit = this.args.onSubmit;
      if (typeof onSubmit !== 'function') {
        return;
      }
      this.loading = true;
      try {
        await onSubmit(this.args.model);
      } finally {
        this.loading = false;
      }
    }
    return false;
  }
}
