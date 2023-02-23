import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';
export default class DependencyOverviewComponent extends Component {
  @service store;
  @action async delete(id) {
    try {
      const dependency = await this.store.peekRecord('dependency', id);
      dependency.deleteRecord();
      await dependency.save();
    } catch (error) {
      console.log('Error!!', error); // eslint-disable-line no-console
    }
  }
}
