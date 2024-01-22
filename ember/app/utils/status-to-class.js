export default function (status) {
  const colorMappings = {
    OUTDATED: 'danger',
    WARNING: 'warning',
    'UP-TO-DATE': 'success',
  };
  return colorMappings[status]
    ? `uk-text-${colorMappings[status]}`
    : 'uk-text-muted';
}
