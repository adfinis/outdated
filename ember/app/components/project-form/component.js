import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import { tracked } from 'tracked-built-ins';

import { emptyChangeset } from 'outdated/utils';
import ProjectValidations from 'outdated/validations/project';

export default class ProjectFormComponent extends Component {
  @service store;
  @service router;

  @service notification;

  @tracked project = emptyChangeset(
    ProjectValidations,
    this.args.project ?? this.store.createRecord('project'),
  );

  saveProject = dropTask(async () => {
    try {
      if (this.project.repoType === 'public') {
        this.project.accessToken = '';
      }

      document
        .querySelectorAll('[data-source-form-submit-button]')
        .forEach((e) => e.click());

      const project = await this.project.save({
        adapterOptions: {
          include:
            'sources,sources.versions,sources.versions.release-version,sources.versions.release-version.dependency,sources.maintainers,sources.maintainers.user',
        },
      });

      this.router.transitionTo('projects.detailed', project.id);
      this.project.accessToken = '';
      this.notification.success('Successfully saved!');
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });

  get repoTypes() {
    return ['public', 'access-token'];
  }

  get users() {
    return this.store.peekAll('user');
  }
}
