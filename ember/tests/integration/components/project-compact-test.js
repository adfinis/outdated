import { render, settled } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { setupIntl } from 'ember-intl/test-support';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';

module('Integration | Component | project-compact', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test('it renders correctly', async function (assert) {
    const project = this.server.create('project', 'withVersions');

    const store = this.owner.lookup('service:store');
    this.project = await store.findRecord('project', project.id, {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
    });
    await render(hbs`<ProjectCompact @project={{this.project}} />`);
    assert.dom('[data-test-dependency-compact]').exists();
    assert.dom(`[data-test-project-link="${this.project.id}"]`).exists();
    assert
      .dom(`[data-test-project-link="${this.project.id}"]`)
      .hasProperty('href', new RegExp(`^.*/projects/${this.project.id}$`));

    assert.dom('[data-test-project-name]').hasText(this.project.name);

    const statusIcons = {
      OUTDATED: 'bolt',
      WARNING: 'warning',
      'UP-TO-DATE': 'check',
      UNDEFINED: 'info',
    };

    for (const [status, icon] of Object.entries(statusIcons)) {
      this.project.status = status;
      await settled(); // eslint-disable-line no-await-in-loop
      assert.dom(`span[icon=${icon}]`).exists();
    }
  });
});
