import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';
module('Integration | Component | form', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders a normal input', async function (assert) {
    await render(hbs`<Form as |f|> <f.input @name="test" /> </Form>`);
    assert.dom('form input').exists();
  });

  test('it renders flatpickr', async function (assert) {
    await render(
      hbs`<Form as |f|> <f.input @name="test" @type="date" /> </Form>`
    );
    assert.dom('form input.ember-flatpickr-input').exists();
  });
  test('it renders powerselect', async function (assert) {
    await render(
      hbs`<Form as |f|> <f.input @name="test" @type="select" /> </Form>`
    );
    assert.dom('form div.ember-power-select-trigger').exists();
    await render(
      hbs`<Form as |f|> <f.input @name="test" @type="select" @multiple={{true}} /> </Form>`
    );
    assert.dom('form input.ember-power-select-trigger-multiple-input').exists();
  });
});
