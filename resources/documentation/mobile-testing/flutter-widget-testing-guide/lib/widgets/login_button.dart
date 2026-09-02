import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  final VoidCallback? onTap;
  final String label;

  const LoginButton({super.key, this.onTap, this.label = 'Log In'});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onTap,
      child: Text(label),
    );
  }
}
