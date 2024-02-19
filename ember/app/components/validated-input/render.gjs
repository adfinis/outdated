import Component from '@glimmer/component';
import getMessages from 'ember-changeset-validations/utils/get-messages';
import { scheduleTask } from 'ember-lifeline';
import PowerSelect from 'ember-power-select/components/power-select';
import PowerSelectMultiple from 'ember-power-select/components/power-select-multiple';
import { or, not, eq } from 'ember-truth-helpers';

import { Date, Select, Text } from './types';

export default class Render extends Component {
  constructor(...args) {
    super(...args);

    if (typeof this.args.hidden === 'boolean') {
      scheduleTask(this, 'actions', this.args.validateModel ?? (() => null));
    }
  }

  get selectComponent() {
    return this.args.multiple ? PowerSelectMultiple : PowerSelect;
  }
  get name() {
    return getMessages().getDescriptionFor(this.args.name);
  }

  <template>
    <div class='uk-margin'>
      {{#if (or @label (not @placeholder))}}
        <@labelComponent @label={{or @label this.name}} />
      {{/if}}
      <div class='uk-form-controls'>

        {{#if (eq @type 'select')}}
          <Select
            @id={{@inputId}}
            @disabled={{@disabled}}
            @isInvalid={{@isInvalid}}
            @isValid={{@isValid}}
            @name={{@name}}
            @setDirty={{@setDirty}}
            @update={{@update}}
            @value={{@value}}
            @options={{@options}}
            @placeholder={{@placeholder}}
            @searchField={{@searchField}}
            @afterOptionsComponent={{@afterOptionsComponent}}
            @optionsComponent={{@optionsComponent}}
            @searchMessage={{@searchMessage}}
            @searchable={{@searchable}}
            @noMatchesMessage={{@noMatchesMessage}}
            @noMatchesMessageComponent={{@noMatchesMessageComponent}}
            @visibleField={{@visibleField}}
            @selectComponent={{this.selectComponent}}
            ...attributes
          />
        {{else if (eq @type 'date')}}
          <Date
            @id={{@inputId}}
            @disabled={{@disabled}}
            @isInvalid={{@isInvalid}}
            @isValid={{@isValid}}
            @options={{@options}}
            @name={{@name}}
            @setDirty={{@setDirty}}
            @update={{@update}}
            @value={{@value}}
            @placeholder={{@placeholder}}
            ...attributes
          />
        {{else}}
          <Text
            placeholder={{@placeholder}}
            id={{@inputId}}
            value={{@value}}
            disabled={{@disabled}}
            @isInvalid={{@isInvalid}}
            @isValid={{@isValid}}
            @name={{@name}}
            @setDirty={{@setDirty}}
            @update={{@update}}
            ...attributes
          />
        {{/if}}
        <@errorComponent />
      </div>
    </div>
  </template>
}
