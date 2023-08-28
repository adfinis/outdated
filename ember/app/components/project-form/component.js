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
    this.args.project ?? this.store.createRecord('project'),
  );

  constructor(...args) {
    super(...args);
    if (this.args.project) {
      scheduleOnce('actions', this, 'initUsers');
    }
  }

  initUsers() {
    this.maintainers = this.project.maintainers;
    this.project.users = this.project.maintainers.map((m) => m.user);
    this.project.primaryMaintainer = this.maintainers?.find(
      (m) => m.isPrimary,
    )?.user;
  }

  saveProject = dropTask(async () => {
    try {
      const created = this.project.isNew;
      const project = await this.project.save();

      this.maintainers
        ?.filter((m) => !this.project.users?.includes(m.user))
        .forEach((m) => m.destroyRecord());
      this.project.users?.forEach((user) => {
        const maintainer = this.maintainers?.find((m) => m.user.id === user.id);
        if (maintainer) {
          maintainer.isPrimary = user.id === this.primaryMaintainer.id;
          if (maintainer.hasDirtyAttributes) maintainer.save();
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

      if (created) {
        project.unloadRecord();
      }

      this.notification.success('Successfully saved!');
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });

  get primaryMaintainer() {
    return (
      this.project.users?.find(
        (u) => u.id === this.project.primaryMaintainer?.id,
      ) ?? this.project.users[0]
    );
  }

  get users() {
    return this.store.peekAll('user');
  }
}
