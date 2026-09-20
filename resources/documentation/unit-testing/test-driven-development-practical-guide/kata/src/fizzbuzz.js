const isMultipleOf = (n, divisor) => n % divisor === 0;

export function fizzBuzz(n) {
  let result = '';
  if (isMultipleOf(n, 3)) result += 'Fizz';
  if (isMultipleOf(n, 5)) result += 'Buzz';
  return result || String(n);
}
