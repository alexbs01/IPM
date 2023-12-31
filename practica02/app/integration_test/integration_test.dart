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

      await tester.pumpAndSettle(const Duration(seconds: 3));

      final Finder input = find.byType(TextFormField);

      await tester.enterText(input, '1233');
      expect(find.text('1233'), findsOneWidget);

      await tester.enterText(input, '123a3bb');
      expect(find.text('123'), findsOneWidget);

      await tester.enterText(input, '1_23345');
      expect(find.text('1'), findsOneWidget);

      await tester.enterText(input, '1233.45');
      expect(find.text('1233.45'), findsOneWidget);

      await tester.enterText(input, '12.33.45');
      expect(find.text('12.33'), findsOneWidget);
    });

    testWidgets('Select an origin currency', (WidgetTester tester) async {
      
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));
      final dropdown = find.byKey(const ValueKey('dropdownSelectCurrency'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verifica que el widget con la clave 'dropdown' está presente
      expect(dropdown, findsOneWidget);

      await tester.tap(dropdown);
      await tester.pumpAndSettle(const Duration(seconds: 5));

      await tester.tap(find.text('EUR'));
      await tester.pumpAndSettle(const Duration(seconds: 5));

      expect(find.text('EUR'), findsOneWidget);
      
    });

    testWidgets('Click on add currency button', (WidgetTester tester) async {
      
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));
      final Finder buttonAdd = find.byIcon(Icons.add); // Busca el widget con el icono de add

      // Verifica que si se pulsa no pasa nada
      expect(buttonAdd, findsOneWidget);
      await tester.tap(buttonAdd);
      expect(buttonAdd, findsOneWidget);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Buscamos el dropdown de las monedas de origen para activar el botón de add currency
      final dropdown = find.byKey(const ValueKey('dropdownSelectCurrency'));

      // Verifica que el widget con la clave 'dropdown' está presente
      expect(dropdown, findsOneWidget);

      // Lo pulsamos y seleccionamos el valor EUR
      await tester.tap(dropdown);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('EUR'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Ahora añadimos la moneda USD
      await tester.tap(buttonAdd);
      await tester.pumpAndSettle(const Duration(seconds: 3));
      expect(buttonAdd, findsNothing);
      await tester.pumpAndSettle(const Duration(seconds: 3));
      await tester.tap(find.text('USD'));

      expect(find.text('USD'), findsOneWidget);
      
    });

    testWidgets('Remove currency', (WidgetTester tester) async {
      
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));
      final Finder buttonAdd = find.byIcon(Icons.add); // Busca el widget con el icono de add

      // Buscamos el dropdown de las monedas de origen para activar el botón de add currency
      final dropdown = find.byKey(const ValueKey('dropdownSelectCurrency'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Lo pulsamos y seleccionamos el valor EUR
      await tester.tap(dropdown);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('EUR'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Ahora añadimos la moneda USD
      await tester.tap(buttonAdd);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('USD'));
      await tester.pumpAndSettle(const Duration(seconds: 5));

      final Finder buttonRemove = find.byIcon(Icons.delete_outline); // Busca el widget con el icono de delete_outline
      await tester.pumpAndSettle(const Duration(seconds: 3));

      expect(buttonRemove, findsOneWidget);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(buttonRemove);
      await tester.pumpAndSettle(const Duration(seconds: 3));
      expect(buttonRemove, findsNothing);
      
    });

    testWidgets('Doing an exchange', (WidgetTester tester) async {
      
      app.main();
      await tester.pumpAndSettle(const Duration(seconds: 3));
      final Finder buttonAdd = find.byIcon(Icons.add); // Busca el widget con el icono de add

      // Buscamos el dropdown de las monedas de origen para activar el botón de add currency
      final dropdown = find.byKey(const ValueKey('dropdownSelectCurrency'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Lo pulsamos y seleccionamos el valor EUR
      await tester.tap(dropdown);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('EUR'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Ahora añadimos la moneda USD
      await tester.tap(buttonAdd);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.text('USD'));
      await tester.pumpAndSettle(const Duration(seconds: 5));

      final Finder input = find.byType(TextFormField);
      await tester.enterText(input, '1');
      await tester.pumpAndSettle(const Duration(seconds: 3));

      expect(find.text('1.05'), findsOneWidget);
    });


  });
}
