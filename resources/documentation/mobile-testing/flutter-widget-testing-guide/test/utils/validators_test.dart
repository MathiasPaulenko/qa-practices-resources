import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_test_app/utils/validators.dart';

void main() {
  group('email validator', () {
    test('returns error for invalid email', () {
      expect(validateEmail('not-an-email'), 'Invalid email');
    });

    test('returns null for valid email', () {
      expect(validateEmail('qa@qa-practices.com'), isNull);
    });

    test('returns error for empty string', () {
      expect(validateEmail(''), 'Email is required');
    });
  });
}
