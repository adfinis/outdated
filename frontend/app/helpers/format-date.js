import { helper } from '@ember/component/helper';

export function formatDate([date]) {
  if (!(date instanceof Date)) {
    return '';
  }

  return date.toLocaleDateString('de-CH', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

export default helper(formatDate);
