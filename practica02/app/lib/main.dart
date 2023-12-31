import 'package:app/view/screens/home_mobile.dart';
import 'package:app/view/screens/home_tablet.dart';
import 'package:app/view_model/currencys.dart';
import 'package:app/view_model/current_currencys.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    var shortestSide = MediaQuery.of(context).size.shortestSide;
    final bool useMobileLayout = shortestSide < 600;

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => Currencys()),
        ChangeNotifierProvider(create: (context) => CurrentCurrencys()),
      ],
      child: MaterialApp(
        title: 'App exchanges',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity
        ),
        home: useMobileLayout? const HomeMobile() : const HomeTablet(),
      ),
    );
  }
}
