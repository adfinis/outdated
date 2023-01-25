import { module, test } from 'qunit';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { render, settled } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';

module('Integration | Component | project-compact', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test('project-compact renders correctly', async function (assert) {
    const project = this.server.create('project', 'withVersions');
    let store = this.owner.lookup('service:store');
    this.project = await store.findRecord('project', project.id, {
      include: 'dependencyVersions,dependencyVersions.dependency',
    });
    await render(hbs`<ProjectCompact  @project={{this.project}} />`);

    assert.dom(`[data-test-project-link="${this.project.id}"]`).exists();
    assert
      .dom(`[data-test-project-link="${this.project.id}"]`)
      .hasProperty('href', new RegExp(`^.*/projects/${this.project.id}$`));

    assert.dom('[data-test-project-name]').hasText(this.project.name);

    assert
      .dom('[data-test-project-status]')
      .hasClass(`text-${this.project.status}`);

    this.project.status = 'OUTDATED';
    await settled();
    assert.dom('span[icon=bolt]').exists();
    this.project.status = 'WARNING';
    await settled();
    assert.dom('span[icon=warning]').exists();
    this.project.status = 'UP-TO-DATE';
    await settled();
    assert.dom('span[icon=check]').exists();

    assert.dom('[data-test-dependency-compact]').exists();
  });
});
