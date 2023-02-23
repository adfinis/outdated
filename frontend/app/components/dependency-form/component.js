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
    try {
      if (this.args.dependency) {
        this.dependency = await this.store.findRecord(
          'dependency',
          this.args.dependency.id
        );
        this.dependency.name = this.name;

        this.router.transitionTo('manage.dependency');
      } else {
        this.dependency = await this.store.createRecord('dependency', {
          name: this.name,
        });
      }
      await this.dependency.save();
      this.name = '';
      console.log('Success!'); // eslint-disable-line no-console
    } catch (error) {
      this.dependency.rollbackAttributes();
      console.log('Error', error); // eslint-disable-line no-console
    }
  }
}
