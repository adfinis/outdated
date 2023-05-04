import Controller from '@ember/controller';
import { action } from '@ember/object';
import { service } from '@ember/service';
import emptyChangeset from 'outdated/utils/empty-changeset';
import ProjectValidations from 'outdated/validations/project';
import { tracked } from 'tracked-built-ins';

export default class ProjectsCreateNewController extends Controller {
  // Services
  @service store;
  @service notification;

  @tracked project = emptyChangeset(
    ProjectValidations,
    this.store.createRecord('project')
  );

  @action async saveProject() {
    try {
      const project = await this.project.save();
      this.transitionToRoute('projects.project-detailed', project.id);
      this.notification.success('Successfully saved!', {
        pos: 'bottom-right',
      });
    } catch (e) {
      this.notification.danger(e);
    }
  }
}
