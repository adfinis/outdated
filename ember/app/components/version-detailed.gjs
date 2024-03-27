import { LinkTo } from '@ember/routing';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import formatDate from 'ember-intl/helpers/format-date';
import UkIcon from 'ember-uikit/components/uk-icon';
import startCase from 'lodash/startCase';

import {
  ProjectCell,
  MaintainersCell,
  EndOfLifeCell,
  DependencyCell,
} from './cells';
import Table from './table';

import { statusToClass } from 'outdated/utils';

export default class VersionDetailedComponent extends Component {
  @service store;

  get projects() {
    return this.store
      .peekAll('project')
      .filter((project) =>
        project.versionedDependencies.find(
          (version) => version.id === this.args.version.id,
        ),
      );
  }

  get data() {
    return this.projects.map((project) => ({
      component: <template>
        <tr class={{statusToClass project.status}}>{{yield}}</tr>
      </template>,
      values: {
        name: <template><ProjectCell @project={{project}} /></template>,
        maintainers: project.maintainers.length
          ? <template>
              <MaintainersCell @maintainers={{project.maintainers}} />
            </template>
          : undefined,
      },
    }));
  }

  get cells() {
    const version = this.args.version;
    const dependency = version.releaseVersion.dependency;
    return Object.entries({
      dependency: <template>
        <DependencyCell @dependency={{dependency}} />
      </template>,
      releaseVersion: <template>{{formatDate version.releaseDate}}</template>,
      endOfLife: <template>
        <EndOfLifeCell
          class={{statusToClass version.status}}
          @version={{version}}
        />
      </template>,
    }).map(([label, value]) => ({ label: startCase(label), value }));
  }

  <template>
    <div class='detailed-header'>
      <h1>
        <LinkTo
          @route='dependencies.detailed'
          @model={{@version.releaseVersion.dependency.id}}
          data-test-version-name
        >
          {{@version.name}}
        </LinkTo>
        {{@version.version}}
      </h1>

      <a href='{{@version.url}}' data-test-version-link>
        <UkIcon @icon='link' @ratio={{3}} />
      </a>
    </div>

    <hr class='seperator' />
    <div class='uk-margin-top'>
      <ul
        class='uk-list uk-flex uk-flex-between uk-flex-stretch uk-margin-remove'
      >
        {{#each this.cells as |cell|}}
          <li class='uk-margin-remove'><strong
              class='uk-display-block'
            >{{cell.label}}</strong><span
              class='uk-width-1-1 center'
            >{{cell.value}}</span></li>
        {{/each}}
      </ul>
    </div>
    <hr class='uk-divider-icon' />
    <Table @title='Used in' @data={{this.data}} as |t|>
      <t.head />
      <t.body />
    </Table>
  </template>
}
