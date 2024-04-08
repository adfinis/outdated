import { concat } from '@ember/helper';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import perform from 'ember-concurrency/helpers/perform';
import { scheduleTask } from 'ember-lifeline';
import { pageTitle } from 'ember-page-title';
import { eq, gt } from 'ember-truth-helpers';
import { tracked } from 'tracked-built-ins';

import Form from './form';

import { emptyChangeset } from 'outdated/utils';
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
      scheduleTask(this, 'actions', () => {
        this.maintainers = this.project.maintainers;
        this.project.users = this.project.maintainers.map((m) => m.user);
        this.project.primaryMaintainer = this.maintainers?.find(
          (m) => m.isPrimary,
        )?.user;
      });
    }
  }

  saveProject = dropTask(async () => {
    try {
      if (this.project.repoType === 'public') {
        this.project.accessToken = '';
      }

      const project = await this.project.save({
        adapterOptions: {
          include:
            'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency,maintainers,maintainers.user',
        },
      });

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
      this.project.accessToken = '';
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

  get repoTypes() {
    return ['public', 'access-token'];
  }
  <template>
    {{pageTitle @project.name}}

    <Form
      @name={{if
        @project
        (concat 'Edit project ' @project.name)
        'Track new Project'
      }}
      @model={{this.project}}
      @onSubmit={{perform this.saveProject}}
      as |f|
    >
      <f.input @name='name' />
      <div class='uk-margin'>
        <label class='uk-form-label'>Repo</label>
        <div class='repo-inputs'>
          <f.input @name='repo' @raw={{true}} />
          <f.input
            @name='repoType'
            @type='select'
            @options={{this.repoTypes}}
            @raw={{true}}
          />
        </div>
      </div>

      <f.input
        @name='accessToken'
        type='password'
        autocomplete='off'
        @hidden={{eq this.project.repoType 'public'}}
      />

      <f.input
        @name='users'
        @type='select'
        @label='Maintainers'
        @multiple={{true}}
        @value={{this.project.users}}
        @options={{this.users}}
        @searchField='searchField'
        @visibleField='fullName'
      />
      {{#if (gt this.project.users.length 1)}}
        <f.input
          @name='primaryMaintainer'
          @type='select'
          @options={{this.project.users}}
          @value={{this.primaryMaintainer}}
          @searchField='searchField'
          @visibleField='fullName'
        />
      {{/if}}
      <f.button @loading={{this.saveProject.isRunning}} />
    </Form>
  </template>
}
