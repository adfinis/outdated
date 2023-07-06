import sortBy from 'ember-composable-helpers/helpers/sort-by';

<template>
  <h2 class='table-header'>Maintainers</h2>
  <hr class='seperator' />
  {{#if @maintainers}}
    <table>
      <thead>
        <tr>
          <th>Username </th>
          <th>Email Address</th>
        </tr>
      </thead>
      <tbody>
        {{#each (sortBy 'isPrimary' @maintainers) as |maintainer|}}
          <tr>
            <td>
              {{maintainer.user.username}}
            </td>
            <td>
              {{maintainer.user.email}}
            </td>
          </tr>
        {{/each}}
      </tbody>
    </table>
  {{else}}
    <div class='none-yet' data-test-versioned-dependencies-none>
      <span class='text-undefined'>No maintainers yet</span>
    </div>
  {{/if}}
</template>
