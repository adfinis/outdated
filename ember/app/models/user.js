import Model, { attr } from '@ember-data/model';

export default class UserModel extends Model {
  @attr idpId;
  @attr firstName;
  @attr lastName;
  @attr email;
  @attr username;

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  }
  get searchField() {
    return `${this.username} ${this.fullName} ${this.email}`;
  }
}
