import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_test_app/widgets/login_button.dart';

void main() {
  testWidgets('login button golden', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: Scaffold(body: LoginButton())),
    );
    await expectLater(
      find.byType(LoginButton),
      matchesGoldenFile('goldens/login_button.png'),
    );
  });
}
