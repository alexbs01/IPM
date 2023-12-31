// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('ent-to-end test', () { 
    testWidgets('Numbers that I can write in the input', (WidgetTester tester) async {

      app.main();

      await tester.testTextInput.receiveAction(TextInputAction.done);
      await tester.pump();

      expect(find.text(''), findsOneWidget);
      await tester.enterText(find.byType(TextFormField), '1233');
      expect(find.text('1233'), findsOneWidget);

      await tester.enterText(find.byType(TextFormField), '123a3bb');
      expect(find.text('123'), findsOneWidget);

      await tester.enterText(find.byType(TextFormField), '1_23345');
      expect(find.text('1'), findsOneWidget);

      await tester.enterText(find.byType(TextFormField), '1233.45');
      expect(find.text('1233.45'), findsOneWidget);

      await tester.enterText(find.byType(TextFormField), '12.33.45');
      expect(find.text('12.33'), findsOneWidget);
    });

    testWidgets('Select an origin currency', (WidgetTester tester) async {
      
      app.main();
      final Finder dropdown = find.byType(DropdownButtonFormField);

      await tester.tap(dropdown);

      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('USD'));
      
    });

  });
}
