import { fn } from '@ember/helper';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import changeset from 'ember-changeset/helpers/changeset';
import { dropTask } from 'ember-concurrency';
import perform from 'ember-concurrency/helpers/perform';
import UkButton from 'ember-uikit/components/uk-button';

import Form from './form';
import Modal from './modal';

import ReleaseVersionValidations from 'outdated/validations/release-version';

export default class EOLForm extends Component {
  @service notification;

  constructor(...args) {
    super(...args);
    this.args.version.endOfLifeDate = this.args.version.endOfLife;
  }

  saveReleaseVersion = dropTask(async (data) => {
    try {
      const changes = await data.changes;
      if (changes.length) {
        const releaseVersion = this.args.version.releaseVersion;
        releaseVersion.endOfLife = changes[0].value;
        await releaseVersion.save();
      }

      this.args.setIsEditing(false);
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });

  <template>
    <Modal
      @title={{@version.releaseVersion.name}}
      @visible={{@isEditing}}
      as |m|
    >
      <Form
        @model={{changeset @version ReleaseVersionValidations}}
        @onSubmit={{perform this.saveReleaseVersion}}
        as |f|
      >
        <m.body>
          <f.input @name='endOfLifeDate' @type='date' />
        </m.body>
        <m.footer class='uk-flex uk-flex-between'>
          <f.button
            @loading={{this.saveReleaseVersion.running}}
            @disabled={{this.saveReleaseVersion.running}}
          />
          <UkButton
            @type='button'
            @label='cancel'
            @color='danger'
            @onClick={{fn @setIsEditing false}}
          />
        </m.footer>
      </Form>
    </Modal>
  </template>
}
