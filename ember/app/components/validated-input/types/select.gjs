import { action, get } from '@ember/object';
import Component from '@glimmer/component';
import or from 'ember-truth-helpers/helpers/or';
export default class SelectComponent extends Component {
  @action
  onUpdate(value) {
    this.args.update(value);
  }
  <template>
    <@selectComponent
      @searchEnabled={{true}}
      @options={{@options}}
      @selected={{@value}}
      @onChange={{this.onUpdate}}
      @onClose={{@setDirty}}
      @searchField={{@searchField}}
      @placeholder={{@placeholder}}
      @renderInPlace={{true}}
      @afterOptionsComponent={{@afterOptionsComponent}}
      @optionsComponent={{@optionsComponent}}
      @searchMessage={{@searchMessage}}
      @noMatchesMessage={{@noMatchesMessage}}
      @noMatchesMessageComponent={{@noMatchesMessageComponent}}
      id={{@inputId}}
      class='{{if @isValid "is-valid "}} {{if @isInvalid "is-invalid"}}'
      as |name|
    >
      {{or (get name (or @visibleField @searchField)) name}}
    </@selectComponent>
  </template>
}
