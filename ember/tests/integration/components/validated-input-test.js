import { render } from '@ember/test-helpers';
import { Changeset } from 'ember-changeset';
import { hbs } from 'ember-cli-htmlbars';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | validated-input ', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders a text input with value', async function (assert) {
    await render(hbs`<ValidatedInput @name='test' @value='foo' />`);
    assert.dom('input').hasValue('foo');
  });

  test('it renders inputs with value from model', async function (assert) {
    this.set('model', new Changeset({ name: 'foo' }));

    await render(hbs`<ValidatedInput @name='name' @model={{this.model}} />`);

    assert.dom('input').hasValue('foo');
  });
  test('it renders inputs with set value instead of the models value', async function (assert) {
    this.set('model', new Changeset({ name: 'foo' }));

    await render(
      hbs`<ValidatedInput @name='name' @value='bar' @model={{this.model}} />`,
    );

    assert.dom('input').hasValue('bar');
  });
  test('it renders disabled inputs', async function (assert) {
    await render(hbs`<ValidatedInput @disabled={{true}} />`);
    assert.dom('input').isDisabled();
  });

  test('it renders inputs with placeholder', async function (assert) {
    await render(hbs`<ValidatedInput @placeholder='test' />`);

    assert.dom('input').hasAttribute('placeholder', 'test');
  });
});
