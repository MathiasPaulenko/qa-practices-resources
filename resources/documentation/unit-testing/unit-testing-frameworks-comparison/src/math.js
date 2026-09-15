// math.js
export function sum(a, b) {
  return a + b;
}

export async function asyncFetch() {
  const { fetchData } = await import('./api');
  return fetchData();
}
