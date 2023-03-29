import Transform from '@ember-data/serializer/transform';

export default class DjangoDateTransform extends Transform {
  deserialize(serialized) {
    return serialized ? new Date(serialized) : null;
  }

  serialize(deserialized) {
    return deserialized instanceof Date
      ? deserialized.toISOString().slice(0, 10)
      : null;
  }
}
