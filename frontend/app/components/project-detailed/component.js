import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';

export default class ProjectDetailedComponent extends Component {
  @service notification;
  @service store;
  @tracked loading = false;

  @action
  async syncProject() {
    try {
      this.loading = true;
      // post request to the api endpoint to sync the project
      const request = await fetch(`/projects/${this.args.project.id}/sync`, {
        method: 'POST',
      });
      if (request.ok) {
        this.notification.success('Project synced successfully');
      } else if (request.status === 404) {
        this.notification.danger('Project not found');
      } else if (request.status === 500) {
        this.notification.danger('An error occurred while syncing the project');
      }
    } catch (e) {
      this.notification.danger(e);
    }
    this.loading = false;
    this.store.findRecord('project', this.args.project.id);
  }
}
