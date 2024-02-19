import { action, get } from '@ember/object';
import { guidFor } from '@ember/object/internals';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import join from 'ember-composable-helpers/helpers/join';
import { and } from 'ember-truth-helpers';

import Render from './validated-input/render';

const Error = <template>
  <small data-test-error id={{@id}} class='uk-text-danger' ...attributes>
    {{yield}}
    {{join ', ' @errors}}
  </small>
</template>;

const Label = <template>
  <label data-test-label class='uk-form-label' for={{@inputId}}>
    {{@label}}
  </label>
</template>;

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

  <template>
    <Render
      @label={{@label}}
      @type={{this.type}}
      @disabled={{@disabled}}
      @value={{this._val}}
      @options={{@options}}
      @name={{@name}}
      @multiple={{@multiple}}
      @inputId={{@inputId}}
      @isValid={{this.isValid}}
      @isInvalid={{this.isInvalid}}
      @model={{@model}}
      @placeholder={{@placeholder}}
      @update={{this.update}}
      @searchField={{@searchField}}
      @visibleField={{@visibleField}}
      @setDirty={{this.setDirty}}
      @submitted={{@submitted}}
      @afterOptionsComponent={{@afterOptionsComponent}}
      @optionsComponent={{@optionsComponent}}
      @searchMessage={{@searchMessage}}
      @noMatchesMessage={{@noMatchesMessage}}
      @noMatchesMessageComponent={{@noMatchesMessageComponent}}
      @errorComponent={{if
        (and this.showValidity this.errors)
        (component Error errors=this.errors id=this.errorId)
      }}
      @labelComponent={{component Label inputId=@inputId}}
      ...attributes
    />
  </template>
}
