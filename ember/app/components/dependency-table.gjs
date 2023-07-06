import DependencyDetailed from './dependency-detailed';

<template>
  <h2 class='table-header'>Dependencies</h2>
  <hr class='seperator' />
  {{#if @versionedDependencies}}
    <table>
      <thead>
        <tr>
          <th>Dependency</th>
          <th>Version</th>
          <th>End of Life</th>
          <th>Release Date</th>
        </tr>
      </thead>
      <tbody>
        {{#each @versionedDependencies as |version|}}
          <DependencyDetailed @version={{version}} />
        {{/each}}

      </tbody>
    </table>
  {{else}}
    <div class='none-yet' data-test-versioned-dependencies-none>
      <span class='text-undefined'>No dependencies yet</span>
    </div>
  {{/if}}
</template>
