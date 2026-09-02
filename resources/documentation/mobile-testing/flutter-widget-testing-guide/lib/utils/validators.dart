String? validateEmail(String input) {
  if (input.isEmpty) return 'Email is required';
  final regex = RegExp(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$');
  if (!regex.hasMatch(input)) return 'Invalid email';
  return null;
}
