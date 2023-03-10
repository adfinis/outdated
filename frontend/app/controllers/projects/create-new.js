import Conroller from '@ember/controller';
import DependencyValidations from 'outdated/validations/dependency';
import DependencyVersionValidations from 'outdated/validations/dependency-version';
import ProjectValidations from 'outdated/validations/project';
export default class ProjectsCreateNewController extends Conroller {
  DependencyValidations = DependencyValidations;
  DependencyVersionValidations = DependencyVersionValidations;
  ProjectValidations = ProjectValidations;
}
