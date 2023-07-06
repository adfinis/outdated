import formatDate from 'ember-intl/helpers/format-date';
import or from 'ember-truth-helpers/helpers/or';

import statusToClass from 'outdated/helpers/status-to-class';

<template>
  <tr class='{{statusToClass @version.status}}'>
    <td data-test-version-dependency-name>
      {{@version.name}}
    </td>
    <td data-test-version-version>
      {{@version.version}}
    </td>
    <td data-test-version-end-of-life>
      {{or (formatDate @version.endOfLife) 'missing'}}
    </td>
    <td data-test-version-release-date>
      {{formatDate @version.releaseDate}}
    </td>
  </tr>
</template>
