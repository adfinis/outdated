import { module, test } from 'qunit';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
module('Integration | Component | dependency-compact', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  test('dependency-compact renders correctly', async function (assert) {
    this.version = await this.server.create('version');

    await render(hbs`<DependencyCompact @version={{this.version}}/>`);

    assert
      .dom('[data-test-dependency-compact]')
      .hasText(`${this.version.dependency.name} ${this.version.version}`);
  });
});
