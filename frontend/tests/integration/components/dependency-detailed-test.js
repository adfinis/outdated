import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';
module('Integration | Component | dependency-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  test('it renders correctly', async function (assert) {
    const store = this.owner.lookup('service:store');
    this.version = await store.findRecord(
      'version',
      await this.server.create('version').id,
      {
        include: 'releaseVersion,releaseVersion.dependency',
      }
    );

    await render(hbs`<DependencyDetailed @version={{this.version}} />`);
    assert
      .dom('[data-test-version-status]')
      .hasClass(`text-${this.version.status}`);
    assert
      .dom('[data-test-version-dependency-name]')
      .hasText(this.version.name);
    assert.dom('[data-test-version-version]').hasText(this.version.version);
    assert.dom('[data-test-version-release-date]').exists();
  });
});
