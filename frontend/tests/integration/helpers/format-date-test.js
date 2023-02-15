import { render } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupRenderingTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';

module('Integration | Helper | format-date', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders the correctly formatted date', async function (assert) {
    this.set('date', new Date('2007-12-12'));

    await render(hbs`{{format-date this.date}}`);

    assert.dom(this.element).hasText('12.12.2007');

    this.set('date', new Date('1543-09-12'));

    assert.dom(this.element).hasText('12.09.1543');
  });
});
