import { Changeset } from 'ember-changeset';
import lookupValidator from 'ember-changeset-validations';

export default function emptyChangeset(validations, model = null) {
  return Changeset(model ?? {}, lookupValidator(validations), validations);
}
