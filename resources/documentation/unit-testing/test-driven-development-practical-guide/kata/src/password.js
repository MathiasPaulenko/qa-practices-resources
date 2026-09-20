const MIN_PASSWORD_LENGTH = 8;

export function validatePassword(password) {
  if (typeof password !== 'string' || password.length < MIN_PASSWORD_LENGTH) {
    return false;
  }
  const hasUppercase = /[A-Z]/.test(password);
  const hasDigit = /\d/.test(password);
  return hasUppercase && hasDigit;
}
