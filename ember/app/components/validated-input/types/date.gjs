import { action } from '@ember/object';
import Component from '@glimmer/component';
import EmberFlatpickr from 'ember-flatpickr/components/ember-flatpickr';
import or from 'ember-truth-helpers/helpers/or';
export default class DateInputComponent extends Component {
  @action
  onUpdate(value) {
    this.args.update(value[0]);
  }
  <template>
    <EmberFlatpickr
      placeholder={{@placeholder}}
      @dateFormat={{or @dateFormat 'Y-m-d'}}
      @date={{or @value null}}
      @onChange={{this.onUpdate}}
      @onClose={{@setDirty}}
      @allowInput={{or @allowInput true}}
      class='uk-input {{if @isValid "is-valid"}} {{if @isInvalid "is-invalid"}}'
    />
  </template>
}
