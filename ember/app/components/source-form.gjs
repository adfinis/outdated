import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import perform from 'ember-concurrency/helpers/perform';
import { scheduleTask } from 'ember-lifeline';
import { lt, or } from 'ember-truth-helpers';
import { tracked } from 'tracked-built-ins';

import Form from './form';

import { emptyChangeset } from 'outdated/utils';
import SourceValidations from 'outdated/validations/source';

export default class SourceForm extends Component {
  @service store;
  @service notification;

  @tracked source = emptyChangeset(SourceValidations, this.args.source);

  constructor(...args) {
    super(...args);

    scheduleTask(this, 'actions', () => {
      const source = this.args.source;
      source.users = source.maintainers.map((m) => m.user);
      source.primaryMaintainer = source.maintainers.find(
        (m) => m.isPrimary,
      )?.user;
    });
  }

  get primaryMaintainer() {
    return (
      this.source.users?.find(
        (u) => u.id === this.source.primaryMaintainer?.id,
      ) ?? this.source.users[0]
    );
  }

  get users() {
    return this.store.peekAll('user');
  }

  saveMaintainers = dropTask(async () => {
    try {
      this.source.maintainers
        ?.filter(
          (m) => !this.source.users?.map((u) => u.id).includes(m.user.id),
        )
        .forEach((m) => m.destroyRecord());
      this.source.users
        ?.filter(
          (u) => !this.source.maintainers?.find((m) => m.user.id === u.id),
        )
        .forEach((user) => {
          this.store.createRecord('maintainer', {
            user,
            source: this.args.source,
            isPrimary: user.id === this.primaryMaintainer.id,
          });
        });
      this.source.maintainers.forEach((m) => {
        m.isPrimary = m.user.id === this.primaryMaintainer.id;
        if (m.hasDirtyAttributes) m.save();
      });
      this.store.findRecord('dependency-source', this.source.id, {
        include: 'maintainers,maintainers.user',
      });
      this.notification.success(
        `Successfully saved maintainers for ${this.source.path}`,
      );
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });

  <template>
    <Form
      @onSubmit={{perform this.saveMaintainers}}
      @model={{this.source}}
      @name={{@source.path}}
      as |f|
    >
      <f.input
        @label='Maintainers'
        @name='users'
        @type='select'
        @options={{this.users}}
        @multiple={{true}}
        @searchField='searchField'
        @visibleField='fullName'
      />
      <f.input
        @name='primaryMaintainer'
        @options={{this.source.users}}
        @hidden={{lt (or this.source.users.length 0) 2}}
        @value={{this.primaryMaintainer}}
        @type='select'
        @searchField='searchField'
        @visibleField='fullName'
      />
      <f.button class='uk-hidden' data-source-form-submit-button />
    </Form>
  </template>
}
