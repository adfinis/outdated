import { render, settled } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { setupIntl } from 'ember-intl/test-support';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | project-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test('it renders correctly', async function (assert) {
    const project = await this.server.create('project', 'withSources');
    const store = this.owner.lookup('service:store');

    this.project = await store.findRecord('project', project.id, {
      include:
        'sources,sources.versions,sources.versions.release-version,sources.versions.release-version.dependency,sources.maintainers,sources.maintainers.user',
    });

    await render(hbs`<ProjectDetailed @project={{this.project}} />`);

    assert.dom('[data-test-project-name]').hasText(this.project.name);
    assert
      .dom('[data-test-repo-link]')
      .hasProperty('href', this.project.repoURL);

    assert
      .dom('h2.table-header')
      .exists({ count: this.project.sources.length });

    this.project.versionedDependencies = [];
    await settled();

    assert.dom('[data-test-fallback]').exists();
  });
});
