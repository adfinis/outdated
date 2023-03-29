import Transform from '@ember-data/serializer/transform';

export default class DjangoUrlTransform extends Transform {
  deserialize(serialized) {
    return serialized;
  }

  serialize(deserialized) {
    if (deserialized && !deserialized.startsWith('http')) {
      return `https://${deserialized}`;
    }
    return deserialized;
  }
}
