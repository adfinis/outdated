import { scheduleOnce } from '@ember/runloop';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import { tracked } from 'tracked-built-ins';

import emptyChangeset from 'outdated/utils/empty-changeset';
import ProjectValidations from 'outdated/validations/project';

export default class ProjectFormComponent extends Component {
  @service store;
  @service router;
  @tracked maintainers;

  @service notification;

  @tracked project = emptyChangeset(
    ProjectValidations,
    this.args.project ?? this.store.createRecord('project')
  );

  constructor(...args) {
    super(...args);
    if (this.args.project) {
      scheduleOnce('actions', this, 'initUsers');
    }
  }

  async initUsers() {
    this.maintainers = await this.project.maintainers.slice();
    this.project.users = await Promise.all(
      this.project.maintainers.map((m) => m.user)
    );

    this.project.primaryMaintainer = this.maintainers.find(
      (m) => m.isPrimary
    )?.user;
  }

  saveProject = dropTask(async () => {
    try {
      const project = await this.project.save();

      this.maintainers
        ?.filter(
          (m) => !this.project.users.map((u) => u.id).includes(m.user.get('id'))
        )
        .forEach((m) => m.destroyRecord());
      this.project.users.forEach((user) => {
        const maintainer = this.maintainers?.find(
          (m) => m.user.get('id') === user.id
        );
        if (maintainer) {
          maintainer.isPrimary = user === this.primaryMaintainer;
          maintainer.save();
        } else {
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
      this.notification.success('Successfully saved!');
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });

  get primaryMaintainer() {
    return (
      this.project.users.find((u) => u === this.project.primaryMaintainer) ??
      this.project.users[0]
    );
  }

  get users() {
    return this.store.peekAll('user');
  }
}
