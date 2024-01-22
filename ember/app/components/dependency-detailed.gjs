import { service } from '@ember/service';
import Component from '@glimmer/component';
import UkIcon from 'ember-uikit/components/uk-icon';

import { VersionCell, ProjectCell, EndOfLifeCell } from './cells';
import Table from './table';

import { statusToClass, orderByEOL } from 'outdated/utils';

export default class DependencyDetailedComponent extends Component {
  @service store;

  get versions() {
    return orderByEOL(
      this.store
        .peekAll('version')
        .filter(
          (version) =>
            version.releaseVersion.dependency.id === this.args.dependency.id,
        ),
    );
  }

  get projects() {
    const getEOL = (project) =>
      project.versionedDependencies.find(
        (v) => v.releaseVersion.dependency.id === this.args.dependency.id,
      ).releaseVersion.endOfLife;
    return orderByEOL(
      this.store
        .peekAll('project')
        .filter(
          (project) =>
            project.versionedDependencies.filter(
              (version) =>
                version.releaseVersion.dependency.id ===
                this.args.dependency.id,
            ).length,
        ),
      getEOL,
    );
  }

  get data() {
    return orderByEOL(
      this.versions.map((version) => ({
        component: <template>
          <tr class={{statusToClass version.status}}>{{yield}}</tr>
        </template>,
        values: {
          version: <template><VersionCell @version={{version}} /></template>,
          endOfLife: <template>
            <EndOfLifeCell @version={{version}} />
          </template>,
          releaseDate: version.releaseDate,
        },
      })),
    );
  }

  get projectData() {
    return this.projects.map((project) => {
      const version = project.versionedDependencies.find(
        (version) =>
          version.releaseVersion.dependency.id === this.args.dependency.id,
      );
      return {
        component: <template>
          <tr class={{statusToClass version.status}}>{{yield}}</tr>
        </template>,
        values: {
          project: <template><ProjectCell @project={{project}} /></template>,
          version: <template><VersionCell @version={{version}} /></template>,
        },
      };
    });
  }

  <template>
    <div class='detailed-header'>
      <h1 data-test-project-name>
        {{@dependency.name}}
      </h1>

      <a href='{{@dependency.url}}' data-test-dependency-link>
        <UkIcon @icon='link' @ratio={{3}} />
      </a>
    </div>

    <hr class='seperator' />

    <Table @title='Versions' @data={{this.data}} as |t|>
      <t.head />
      <t.body />
    </Table>

    <Table @title='Used in' @data={{this.projectData}} as |t|>
      <t.head />
      <t.body />
    </Table>
  </template>
}
