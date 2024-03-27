import { concat } from '@ember/helper';
import { LinkTo } from '@ember/routing';
import formatDate from 'ember-intl/helpers/format-date';
import { or } from 'ember-truth-helpers';
import UkCard from 'ember-uikit/components/uk-card';
import UkIcon from 'ember-uikit/components/uk-icon';
import ukTooltip from 'ember-uikit/modifiers/uk-tooltip';

import statusToClass from 'outdated/helpers/status-to-class';

function icon(status) {
  const stateIconDict = {
    OUTDATED: 'bolt',
    WARNING: 'warning',
    'UP-TO-DATE': 'check',
    UNDEFINED: 'info',
  };
  return stateIconDict[status];
}

function version(project) {
  return project.sources.at(0)?.versions.at(0);
}

const Dependency = <template>
  <span
    data-test-dependency-compact
    {{(if
      @version
      (modifier
        ukTooltip (concat 'EOL: ' (formatDate @version.endOfLife)) pos='bottom'
      )
    )}}
  >
    {{or @version.requirements 'No dependencies yet'}}
  </span>
</template>;

<template>
  <div class='project-compact'>
    <UkCard as |c|>
      <LinkTo
        @route='projects.detailed'
        data-test-project-link='{{@project.id}}'
        @model={{@project}}
      >
        <h3 data-test-project-name class='title-compact'>
          {{@project.name}}
        </h3>
      </LinkTo>
      <c.body class='{{statusToClass @project.status}}'>
        <UkIcon @icon='{{icon @project.status}}' @ratio={{4}} />
        <Dependency @version={{version @project}} />
      </c.body>
    </UkCard>
  </div>
</template>
