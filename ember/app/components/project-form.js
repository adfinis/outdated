import { action } from '@ember/object';
import { scheduleOnce } from '@ember/runloop';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from 'tracked-built-ins';

import emptyChangeset from 'outdated/utils/empty-changeset';
import ProjectValidations from 'outdated/validations/project';

export default class ProjectFormComponent extends Component {
  // Services
  @service store;
  @service router;
  @service notification;

  @tracked project = emptyChangeset(
    ProjectValidations,
    this.args.project ?? this.store.createRecord('project')
  );
  @tracked editing = !!this.args.project;

  constructor(...args) {
    super(...args);
    if (this.args.project) {
      scheduleOnce('actions', this, 'initUsers');
    }
  }

  initUsers() {
    this.project.users = this.users.filter((u) =>
      this.maintainers
        .map((maintainer) => maintainer.user.get('id'))
        .includes(u.id)
    );
    this.project.primaryMaintainer =
      this.project.users.find(
        (u) =>
          u.id ===
          this.maintainers
            .find((maintainer) => maintainer.isPrimary)
            ?.user?.get('id')
      ) ?? this.project.users[0];
  }

  @action
  async saveProject() {
    try {
      const project = await this.project.save();
      this.maintainers.forEach((maintainer) => {
        if (
          !this.project.users
            .map((u) => u.id)
            .includes(maintainer.user.get('id'))
        ) {
          maintainer.destroyRecord();
        } else {
          maintainer.isPrimary =
            maintainer.user.get('id') === this.primaryMaintainer.id;
          maintainer.save();
        }
      });

      this.project.users.forEach((user) => {
        if (!this.maintainers.map((m) => m.user.get('id')).includes(user.id)) {
          this.store
            .createRecord('maintainer', {
              user,
              project,
              isPrimary: user === this.primaryMaintainer,
            })
            .save();
        }
      });

      this.router.transitionTo('projects.detailed', project.id);
      this.notification.success('Successfully saved!', {
        pos: 'bottom-right',
      });
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  }

  get primaryMaintainer() {
    return this.project.users
      ?.map((u) => u.id)
      .includes(this.project.primaryMaintainer?.get('id'))
      ? this.project.primaryMaintainer
      : this.project.users[0];
  }

  get users() {
    return this.store.peekAll('user');
  }

  get maintainers() {
    return this.store.peekAll('maintainer').filter((m) => {
      return m.project.get('id') === this.project.id;
    });
  }
}
