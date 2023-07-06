import { on } from '@ember/modifier';
import { action } from '@ember/object';
import Component from '@glimmer/component';
export default class TextInputComponent extends Component {
  @action
  onUpdate(e) {
    this.args.update(e.target.value);
  }
  <template>
    {{! template-lint-disable require-input-label}}
    <input
      {{on 'input' this.onUpdate}}
      {{on 'blur' @setDirty}}
      class='uk-input {{if @isValid "is-valid"}} {{if @isInvalid "is-invalid"}}'
      ...attributes
    />
  </template>
}
