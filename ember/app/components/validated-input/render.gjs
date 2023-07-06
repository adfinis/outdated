import { ensureSafeComponent } from '@embroider/util';
import Component from '@glimmer/component';
import getMessages from 'ember-changeset-validations/utils/get-messages';
import eq from 'ember-truth-helpers/helpers/eq';
import not from 'ember-truth-helpers/helpers/not';
import or from 'ember-truth-helpers/helpers/or';

import Error from './error';
import Label from './label';
import Date from './types/date';
import Select from './types/select';
import Text from './types/text';

export default class RenderComponent extends Component {
  get selectComponent() {
    return ensureSafeComponent(
      this.args.multiple ? 'power-select-multiple' : 'power-select',
      this
    );
  }
  get name() {
    return getMessages().getDescriptionFor(this.args.name);
  }
  <template>
    <div class='uk-margin'>
      {{#if (or @label (not @placeholder))}}
        <Label @inputId={{@inputId}} @label={{or @label this.name}} />
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
        {{#if @errors}}
          <Error @errors={{@errors}} @id={{@errorId}} />
        {{/if}}
      </div>
    </div>
  </template>
}
