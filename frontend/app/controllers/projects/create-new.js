import Controller from '@ember/controller';
import { action } from '@ember/object';
import { service } from '@ember/service';
import { Changeset } from 'ember-changeset';
import lookupValidator from 'ember-changeset-validations';
import DependencyValidations from 'outdated/validations/dependency';
import DependencyVersionValidations from 'outdated/validations/dependency-version';
import ProjectValidations from 'outdated/validations/project';
import SelectDependencyValidations from 'outdated/validations/select-dependency';
import SelectVersionValidations from 'outdated/validations/select-version';
import { tracked } from 'tracked-built-ins';

function getEmptyChangeset(validations, model = null) {
  return Changeset(model ?? {}, lookupValidator(validations), validations);
}

export default class ProjectsCreateNewController extends Controller {
  DependencyValidations = DependencyValidations;
  DependencyVersionValidations = DependencyVersionValidations;
  ProjectValidations = ProjectValidations;
  SelectDependencyValidations = SelectDependencyValidations;
  SelectVersionValidations = SelectVersionValidations;
  // Services
  @service store;
  @service notification;

  @tracked project = getEmptyChangeset(
    ProjectValidations,
    this.store.createRecord('project')
  );

  @tracked addVersionChangeset = getEmptyChangeset(
    DependencyVersionValidations
  );
  @tracked dependencyChangeset = getEmptyChangeset(SelectDependencyValidations);
  @tracked versionChangeset = getEmptyChangeset(SelectVersionValidations);
  @tracked addDependencyChangeset = getEmptyChangeset(DependencyValidations);

  @tracked selectedDependency = null;

  modalSequence = tracked({
    selectDependency: false,
    selectVersion: false,
    addDependency: false,
    addVersion: false,
  });

  get modals() {
    const maxNum = Math.max(...Object.values(this.modalSequence));
    return Object.entries(this.modalSequence).reduce((acc, [key, value]) => {
      acc[key] = value === maxNum && value !== 0;
      return acc;
    }, {});
  }

  get filteredDependencyVersions() {
    const dep = this.selectedDependency;
    if (!dep) return [];
    return this.store.peekAll('dependencyVersion').filter((dv) => {
      return dv.dependency.get('id') === dep.id;
    });
  }

  @action openModal(modal) {
    const maxNum = Math.max(...Object.values(this.modalSequence));

    if (typeof this.modalSequence[modal] !== 'number') {
      this.modalSequence[modal] = maxNum + 1;
      return;
    }

    const currentnNum = this.modalSequence[modal];

    if (currentnNum === maxNum) {
      return;
    }
    Object.entries(this.modalSequence).forEach(([key, value]) => {
      if (value > currentnNum) {
        this.modalSequence[key] = value - 1;
      }
    });
    this.modalSequence[modal] = maxNum;
  }

  @action closeModal(modal) {
    if (typeof this.modalSequence[modal] !== 'number') {
      return;
    }
    const currentnNum = this.modalSequence[modal];
    for (const [key, value] of Object.entries(this.modalSequence)) {
      if (value > currentnNum) {
        this.modalSequence[key] = value - 1;
      }
    }
    this.modalSequence[modal] = false;
  }

  @action closeModals() {
    Object.keys(this.modalSequence).forEach((key) => {
      this.modalSequence[key] = false;
    });
    this.dependencyChangeset.rollback();
    this.versionChangeset.rollback();
    this.addVersionChangeset.rollback();
    this.addDependencyChangeset.rollback();
    this.selectedDependency = null;
  }

  @action
  async addVersion(dependencyVersion) {
    try {
      const depver = await this.store.createRecord(
        'dependencyVersion',
        dependencyVersion.pendingData
      );
      depver.dependency = this.selectedDependency;
      await depver.save();
      this.project.dependencyVersions.pushObject(depver);
      this.closeModals();
    } catch (e) {
      this.notification.danger(e, { pos: 'bottom-right' });
    }
  }

  @action
  addDependencyVersion(dependencyVersion) {
    this.project.dependencyVersions.pushObject(dependencyVersion.version);
    this.closeModals();
  }

  @action selectDependency(dependency) {
    this.selectedDependency = dependency.dependency;
    this.openModal('selectVersion');
  }

  @action async addDependency(dependency) {
    try {
      const dep = await this.store.createRecord(
        'dependency',
        dependency.pendingData
      );
      this.selectedDependency = await dep.save();
      this.openModal('addVersion');
    } catch (e) {
      this.notification.danger(e, { pos: 'bottom-right' });
    }
  }

  @action async saveProject() {
    try {
      const project = await this.project.save();
      this.transitionToRoute('projects.project-detailed', project.id);
      this.notification.success('Successfully saved!', {
        pos: 'bottom-right',
      });
    } catch (e) {
      this.notification.danger(e, { pos: 'bottom-right' });
    }
  }
}
