import Component from '@glimmer/component';
import { action } from '@ember/object';
import { service } from '@ember/service';
export default class DependencyForm extends Component {
  @service store;
  @action async update(event) {
    this.name = event.target.value;
  }

  @action
  async save(event) {
    event.preventDefault();
    this.store
      .createRecord('dependency', {
        name: this.name,
      })
      .save();
  }
}
