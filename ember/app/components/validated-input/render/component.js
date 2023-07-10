import Component from '@glimmer/component';
import getMessages from 'ember-changeset-validations/utils/get-messages';
import PowerSelect from 'ember-power-select/components/power-select';
import PowerSelectMultiple from 'ember-power-select/components/power-select-multiple';

export default class RenderComponent extends Component {
  get selectComponent() {
    return this.args.multiple ? PowerSelectMultiple : PowerSelect;
  }
  get name() {
    return getMessages().getDescriptionFor(this.args.name);
  }
}
