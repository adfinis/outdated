import { LinkTo } from '@ember/routing';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import perform from 'ember-concurrency/helpers/perform';
import { confirm } from 'ember-uikit';
import UkButton from 'ember-uikit/components/uk-button';
import UkIcon from 'ember-uikit/components/uk-icon';

import { VersionCell, DependencyCell, EndOfLifeCell } from './cells';

import Table from 'outdated/components/table';
import { statusToClass } from 'outdated/utils';

export default class ProjectDetailedComponent extends Component {
  @service notification;
  @service store;
  @service fetch;
  @service router;

  syncProject = dropTask(async () => {
    try {
      // post request to the api endpoint to sync the project
      const project = await this.fetch.fetch(
        `/api/projects/${this.args.project.id}/sync?${new URLSearchParams({
          include:
            'sources,sources.versions,sources.versions.release-version,sources.versions.release-version.dependency,sources.maintainers,sources.maintainers.user',
        })}`,
        {
          method: 'POST',
        },
      );
      if (project.ok) {
        this.notification.success('Project synced successfully');
        await this.store.pushPayload(await project.json());
      } else if (project.status === 404) {
        this.notification.danger('Project not found');
      } else if (project.status === 500) {
        this.notification.danger('An error occurred while syncing the project');
      }
    } catch (e) {
      this.notification.danger(e);
    }
  });

  deleteProject = dropTask(async () => {
    try {
      if (
        !(await confirm(
          `Are you sure you want to delete the project ${this.args.project.name}? This action can't be undone.`,
        ))
      ) {
        return;
      }
      await this.args.project.destroyRecord();
      this.notification.success('Project deleted successfully');
      this.router.transitionTo('projects.index');
    } catch (e) {
      this.notification.danger('An error occurred while deleting the project');
    }
  });

  sourceData(source) {
    return source.versions.map((version) => ({
      component: <template>
        <tr class='{{statusToClass version.status}}'>{{yield}}</tr>
      </template>,
      values: {
        dependency: <template>
          <DependencyCell @dependency={{version.releaseVersion.dependency}} />
        </template>,
        version: <template><VersionCell @version={{version}} /></template>,
        endOfLife: <template><EndOfLifeCell @version={{version}} /></template>,
        releaseDate: version.releaseDate,
      },
    }));
  }

  maintainerData(source) {
    return source.maintainers
      .slice()
      .sort((a, b) => (a.isPrimary - b.isPrimary) * -1)
      .map((m) => ({
        values: {
          username: <template>
            {{#if m.isPrimary}}<UkIcon @icon='star' @ratio={{0.5}} />
            {{/if}}{{m.user.username}}
          </template>,
          email: <template>
            <a
              class='uk-link-text'
              href='mailto:{{m.user.email}}'
            >{{m.user.email}}</a>
          </template>,
        },
      }));
  }

  <template>
    <div class='project-detailed'>

      <div class='detailed-header'>

        <h1 data-test-project-name>
          {{@project.name}}
        </h1>

        <a href='{{@project.repoURL}}' target='blank_' data-test-repo-link>
          <UkIcon @icon='github' @ratio={{3}} />
        </a>

      </div>

      <hr class='seperator' />
      {{#each @project.sources as |source|}}
        <Table
          @data={{this.sourceData source}}
          @fallback='No dependencies yet'
          @title={{source.path}}
          as |t|
        >
          <t.head />
          <t.body />
        </Table>
        <Table @data={{this.maintainerData source}} as |t|>
          <t.head />
          <t.body />
        </Table>
      {{/each}}
      <UkButton
        @label='Sync'
        @loading={{this.syncProject.isRunning}}
        @onClick={{perform this.syncProject}}
      />
      <LinkTo
        @route='projects.detailed.edit'
        class='uk-button uk-button-default'
      >Edit</LinkTo>

      <UkButton
        class='uk-float-right'
        @label='Delete'
        @color='danger'
        @loading={{this.deleteProject.isRunning}}
        @onClick={{perform this.deleteProject}}
      />
    </div>
  </template>
}
