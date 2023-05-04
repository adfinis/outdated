import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import emptyChangeset from 'outdated/utils/empty-changeset';
import EndOfLifeValidations from 'outdated/validations/end-of-life';

export default class DependencyDetailedComponent extends Component {
  @service store;
  @service notification;
  @service router;

  @tracked editModal = false;
  @tracked selected = null;
  @tracked loading = false;
  @tracked changeset = emptyChangeset(EndOfLifeValidations);

  @action
  openModal(version) {
    this.selected = version;
    this.editModal = true;
  }

  @action
  cancel() {
    this.changeset.rollback();
    this.editModal = false;
    this.selected = null;
  }

  @action
  async save(cs) {
    this.loading = true;
    try {
      const releaseVersion = await this.store.findRecord(
        'release-version',
        this.selected.releaseVersion.get('id')
      );
      releaseVersion.endOfLife = cs.endOfLife;
      await releaseVersion.save();
      this.cancel();
      this.router.refresh();
    } catch (e) {
      this.notification.danger(e);
    }
    this.loading = false;
  }
}
