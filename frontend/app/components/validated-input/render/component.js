import Component from '@glimmer/component';

export default class RenderComponent extends Component {
  get selectComponent() {
    return !!this.args.multiple ? 'power-select-multiple' : 'power-select';
  }
}
