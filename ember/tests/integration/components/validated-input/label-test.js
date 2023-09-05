import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | validated-input/label', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    await render(hbs`<ValidatedInput::Label @label={{'test'}} />`);
    assert.dom('[data-test-label]').hasText('test');
  });
});
