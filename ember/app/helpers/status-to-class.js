import { helper } from '@ember/component/helper';

export default helper(function statusToClass(status) {
  const colorMappings = {
    OUTDATED: 'danger',
    WARNING: 'warning',
    'UP-TO-DATE': 'success',
  };
  return colorMappings[status]
    ? `uk-text-${colorMappings[status]}`
    : 'text-undefined';
});
