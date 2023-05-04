import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';
module(
  'Integration | Component | validated-input/types/date',
  function (hooks) {
    setupRenderingTest(hooks);

    test('it renders', async function (assert) {
      await render(hbs`
      <ValidatedInput::Types::Date />
    `);
      assert.dom('input.ember-flatpickr-input').exists();
    });
  }
);
