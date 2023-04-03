import { action, get } from '@ember/object';
import { guidFor } from '@ember/object/internals';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
export default class FormInputComponent extends Component {
  inputId = guidFor(this);

  get errorId() {
    return `${this.inputId}-error`;
  }

  @tracked dirty = false;
  @tracked type = this.args.type ?? 'text';

  get _val() {
    return (
      this.args.value ??
      (this.args.model &&
        this.args.name &&
        get(this.args.model, this.args.name))
    );
  }

  get errors() {
    const errors =
      (this.args.model &&
        get(this.args.model, `error.${this.args.name}.validation`)) ??
      [];

    return errors;
  }

  get isValid() {
    return this.showValidity && !this.errors.length;
  }

  get isInvalid() {
    return this.showValidity && !!this.errors.length;
  }
  get showValidity() {
    return this.args.submitted || this.dirty;
  }

  @action
  setDirty() {
    this.dirty = true;
  }

  @action
  update(value) {
    this.args.model.set(this.args.name, value);
  }
}
