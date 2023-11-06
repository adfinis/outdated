import Transform from '@ember-data/serializer/transform';
import { DateTime } from 'luxon';

export default class DjangoDateTransform extends Transform {
  deserialize(serialized) {
    return serialized ? new Date(serialized) : null;
  }

  serialize(deserialized) {
    return deserialized instanceof Date
      ? DateTime.fromJSDate(deserialized).toISODate()
      : null;
  }
}
