import { render, fillIn, triggerEvent } from '@ember/test-helpers';
import Changeset from 'ember-changeset';
import lookupValidator from 'ember-changeset-validations';
import { hbs } from 'ember-cli-htmlbars';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
import TestValidations from 'outdated/tests/validations/test';

module('Integration | Component | form', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders a normal input', async function (assert) {
    await render(hbs`<Form as |f|> <f.input @name='test' /> </Form>`);
    assert.dom('form input').exists();
  });

  test('it renders flatpickr', async function (assert) {
    await render(
      hbs`<Form as |f|> <f.input @name='test' @type='date' /> </Form>`,
    );
    assert.dom('form input.ember-flatpickr-input').exists();
  });

  test('it renders powerselect', async function (assert) {
    await render(
      hbs`<Form as |f|> <f.input @name='test' @type='select' /> </Form>`,
    );
    assert.dom('form div.ember-power-select-trigger').exists();
    await render(
      hbs`<Form as |f|> <f.input @name='test' @type='select' @multiple={{true}} /> </Form>`,
    );
    assert.dom('form input.ember-power-select-trigger-multiple-input').exists();
  });

  test('it renders errors', async function (assert) {
    this.model = new Changeset(
      {},
      lookupValidator(TestValidations),
      TestValidations,
    );
    await render(
      hbs`<Form as |f|>
  <f.input data-test-input @model={{this.model}} @name='test' />
</Form>`,
    );
    triggerEvent('[data-test-input]', 'blur');
    await fillIn('[data-test-input]', 'foo');
    assert.dom('small[data-test-error]').exists();
    await fillIn('[data-test-input]', 'test');
    assert.dom('small[data-test-error]').doesNotExist();
  });
});
