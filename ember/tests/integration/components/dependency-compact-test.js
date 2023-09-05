import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | dependency-compact', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test('it renders correctly with a version', async function (assert) {
    const store = this.owner.lookup('service:store');
    this.version = await store.findRecord(
      'version',
      await this.server.create('version').id,
      {
        include: 'releaseVersion,releaseVersion.dependency',
      },
    );

    await render(hbs`<DependencyCompact @version={{this.version}} />`);

    assert
      .dom('[data-test-dependency-compact]')
      .hasText(this.version.get('requirements'));
  });

  test('it renders correctly without a version', async function (assert) {
    await render(hbs`<DependencyCompact />`);

    assert.dom('[data-test-dependency-compact]').hasText('No dependencies yet');
  });
});
