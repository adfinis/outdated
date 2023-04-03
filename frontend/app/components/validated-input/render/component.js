import Component from '@glimmer/component';
import getMessages from 'ember-changeset-validations/utils/get-messages';
export default class RenderComponent extends Component {
  get selectComponent() {
    return this.args.multiple ? 'power-select-multiple' : 'power-select';
  }
  get name() {
    return getMessages().getDescriptionFor(this.args.name);
  }
}
