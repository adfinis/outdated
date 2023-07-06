import Component from '@glimmer/component';

export default class ErrorComponent extends Component {
  get errorsAsString() {
    return this.args.errors?.join(', ');
  }

  <template>
    <small data-test-error id={{@id}} class='uk-text-danger' ...attributes>
      {{yield}}{{this.errorsAsString}}
    </small>
  </template>
}
