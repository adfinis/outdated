import { action } from '@ember/object';
import { scheduleOnce } from '@ember/runloop';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
export default class FormComponent extends Component {
  @tracked loading = false;
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
