import { LinkTo } from '@ember/routing';
import Component from '@glimmer/component';
import UkCard from 'ember-uikit/components/uk-card';
import UkIcon from 'ember-uikit/components/uk-icon';

import DependencyCompact from './dependency-compact';

import StatusToClass from 'outdated/helpers/status-to-class';

export default class ProjectCompactComponent extends Component {
  get icon() {
    const stateIconDict = {
      OUTDATED: 'bolt',
      WARNING: 'warning',
      'UP-TO-DATE': 'check',
      UNDEFINED: 'info',
    };
    return stateIconDict[this.args.project.status];
  }
  get version() {
    return this.args.project.versionedDependencies.slice()[0];
  }

  /* eslint-disable no-undef */
  <template>
    <div class='project-compact'>

      <UkCard as |card|>

        <LinkTo
          @route='projects.detailed'
          data-test-project-link='{{@project.id}}'
          @model={{@project}}
        >
          <h3 data-test-project-name class='title-compact'>
            {{@project.name}}
          </h3>
        </LinkTo>

        <card.body class='{{StatusToClass @project.status}}'>

          <UkIcon @icon='{{this.icon}}' @ratio={{4}} />
          <DependencyCompact @version={{this.version}} />

        </card.body>
      </UkCard>
    </div>
  </template>
}
