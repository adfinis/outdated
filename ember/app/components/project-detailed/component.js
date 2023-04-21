import { action } from '@ember/object';
import { service } from '@ember/service';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import fetch from 'fetch';
export default class ProjectDetailedComponent extends Component {
  @service notification;
  @service store;
  @service router;
  @tracked loading = false;

  @action
  async syncProject() {
    try {
      this.loading = true;
      const request = await fetch(`/api/projects/${this.args.project.id}/sync`);
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
    this.router.refresh();
  }
}
