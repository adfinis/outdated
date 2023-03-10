import Component from '@glimmer/component';

export default class ErrorComponent extends Component {
  get errorsAsString() {
    return this.args.errors?.join(', ');
  }
}
