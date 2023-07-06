import { concat } from '@ember/helper';
import formatDate from 'ember-intl/helpers/format-date';
import or from 'ember-truth-helpers/helpers/or';
import { ukTooltip } from 'ember-uikit/modifiers/uk-tooltip';
<template>
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
</template>
