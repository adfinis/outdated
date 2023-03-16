import { render, settled } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';
module('Integration | Component | project-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test('it renders correctly', async function (assert) {
    const project = await this.server.create('project', 'withVersions');
    const store = this.owner.lookup('service:store');

    this.project = await store.findRecord('project', project.id, {
      include: 'dependencyVersions,dependencyVersions.dependency',
    });

    await render(hbs`<ProjectDetailed @project={{this.project}}/>`);

    assert.dom('[data-test-project-name]').hasText(this.project.name);
    assert.dom('[data-test-repo-link]').hasProperty('href', this.project.repo);

    assert
      .dom('tbody>tr')
      .exists({ count: this.project.dependencyVersions.length });

    this.project.dependencyVersions = [];
    await settled();

    assert.dom('[data-test-dependency-versions-none]').exists();
  });
});
