import { get } from '@ember/object';

export default function orderByEOL(items, key = 'endOfLife') {
  const FUTURE = new Date('9999-01-01');
  const orderedItems = items.slice();
  if (typeof key === 'function') {
    return orderedItems.sort(
      (a, b) => (key(a) ?? FUTURE).getTime() - (key(b) ?? FUTURE).getTime(),
    );
  }
  return orderedItems.sort(
    (a, b) =>
      (get(a, key) ?? FUTURE).getTime() - (get(b, key) ?? FUTURE).getTime(),
  );
}
