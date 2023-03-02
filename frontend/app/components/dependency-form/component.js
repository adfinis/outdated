import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
export default class DependencyForm extends Component {
  @service router;
  @service store;

  @tracked name;

  @action async update(event) {
    this.name = event.target.value;
  }

  @action
  async save(event) {
    event.preventDefault();

    const dependency =
      this.args.dependency ?? this.store.createRecord('dependency');
    dependency.name = this.name;

    try {
      await dependency.save();

      this.name = '';

      if (this.args.dependency) {
        this.router.transitionTo('manage.dependency');
      }
    } catch (e) {
      dependency.rollbackAttributes();
    }
  }
}
