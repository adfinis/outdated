import { LinkTo } from '@ember/routing';
import UkButton from 'ember-uikit/components/uk-button';
import UkIcon from 'ember-uikit/components/uk-icon';

import DependencyTable from './dependency-table';
import MaintainerTable from './maintainer-table';

<template>
  <div class='project-detailed'>

    <div class='detailed-header'>

      <h1 data-test-project-name>
        {{@project.name}}
      </h1>

      <a href='{{@project.repo}}' target='blank_' data-test-repo-link>
        <UkIcon @icon='github' @ratio={{3}} />
      </a>

    </div>

    <hr class='seperator' />
    <MaintainerTable @maintainers={{@project.maintainers}} />
    <DependencyTable
      @versionedDependencies={{@project.versionedDependencies}}
    />
    <LinkTo @route='projects.detailed.edit'>
      <UkButton @label='edit' />
    </LinkTo>
  </div>
</template>
