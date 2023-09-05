import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | validated-input/label', function (hooks) {
  setupRenderingTest(hooks);
  test('it renders', async function (assert) {
    await render(hbs`<ValidatedInput::Render
  @labelComponent={{component 'validated-input/label'}}
  @name='test'
  @setDirty={{fn (mut this.dirty) true}}
/>`);

    assert.dom('input').exists();
    assert.dom('label').hasText('Test');
  });
});
