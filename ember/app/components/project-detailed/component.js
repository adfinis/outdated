import { service } from '@ember/service';
import Component from '@glimmer/component';
import { dropTask } from 'ember-concurrency';
import { confirm } from 'ember-uikit';

export default class ProjectDetailedComponent extends Component {
  @service notification;
  @service store;
  @service fetch;
  @service router;

  syncProject = dropTask(async () => {
    try {
      // post request to the api endpoint to sync the project
      const project = await this.fetch.fetch(
        `/api/projects/${this.args.project.id}/sync?${new URLSearchParams({
          include:
            'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
        })}`,
        {
          method: 'POST',
        },
      );
      if (project.ok) {
        this.notification.success('Project synced successfully');
        await this.store.pushPayload(await project.json());
      } else if (project.status === 404) {
        this.notification.danger('Project not found');
      } else if (project.status === 500) {
        this.notification.danger('An error occurred while syncing the project');
      }
    } catch (e) {
      this.notification.danger(e);
    }
  });

  deleteProject = dropTask(async () => {
    try {
      if (
        !(await confirm(
          `Are you sure you want to delete the project ${this.args.project.name}? This action can't be undone.`,
        ))
      ) {
        return;
      }
      await this.args.project.destroyRecord();
      this.notification.success('Project deleted successfully');
      this.router.transitionTo('projects.index');
    } catch (e) {
      this.notification.danger('An error occurred while deleting the project');
    }
  });
}
