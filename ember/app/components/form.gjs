import { hash } from '@ember/helper';
import { on } from '@ember/modifier';
import { action } from '@ember/object';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { scheduleTask } from 'ember-lifeline';
import UkButton from 'ember-uikit/components/uk-button';

import ValidatedInput from 'outdated/components/validated-input';

export default class FormComponent extends Component {
  @tracked loading = false;
  @tracked submitted = false;

  constructor(...args) {
    super(...args);

    if (this.args.model && this.args.model.validate) {
      scheduleTask(this, 'actions', () => this.validateModel);
    }
  }

  @action
  validateModel() {
    this.args.model.validate();
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

  <template>
    <form class='uk-form' autocomplete='off' {{on 'submit' this.submit}}>
      <fieldset class='uk-fieldset'>
        <legend class='uk-legend'>{{@name}}</legend>
        {{yield
          (hash
            model=@model
            loading=this.loading
            input=(component
              ValidatedInput model=@model submitted=this.submitted
            )
            button=(component UkButton label='Save' type='submit')
          )
        }}
      </fieldset>
    </form>
  </template>
}
