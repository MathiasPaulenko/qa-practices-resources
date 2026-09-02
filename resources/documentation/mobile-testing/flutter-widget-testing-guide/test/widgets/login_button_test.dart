import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_test_app/widgets/login_button.dart';

void main() {
  testWidgets('displays correct label', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: Scaffold(body: LoginButton())),
    );
    expect(find.text('Log In'), findsOneWidget);
  });

  testWidgets('calls onTap when pressed', (WidgetTester tester) async {
    bool tapped = false;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: LoginButton(onTap: () => tapped = true),
        ),
      ),
    );
    await tester.tap(find.text('Log In'));
    await tester.pump();
    expect(tapped, isTrue);
  });
}
