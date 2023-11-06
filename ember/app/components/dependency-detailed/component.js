import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { dropTask } from 'ember-concurrency';

import ReleaseVersionValidations from 'outdated/validations/release-version';

export default class DependencyDetailedComponent extends Component {
  @service notification;

  ReleaseVersionValidations = ReleaseVersionValidations;

  @tracked editing = false;

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

      this.editing = false;
    } catch (e) {
      this.notification.danger(e);
      console.error(e);
    }
  });
}
