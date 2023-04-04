import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';
module('Integration | Component | dependency-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  test('it renders correctly', async function (assert) {
    this.version = await this.server.create('dependency-version');

    await render(hbs`<DependencyDetailed @version={{this.version}} />`);
    assert
      .dom('[data-test-version-status]')
      .hasClass(`text-${this.version.status}`);
    assert
      .dom('[data-test-version-dependency-name]')
      .hasText(this.version.dependency.name);
    assert.dom('[data-test-version-version]').hasText(this.version.version);
    assert.dom('[data-test-version-eol-date]').exists();
    assert.dom('[data-test-version-release-date]').exists();
  });
});
