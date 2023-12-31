import 'package:app/view_model/current_currencys.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';


class AddCurrency extends StatelessWidget {
  List<String> currencies;
  AddCurrency({super.key, required this.currencies});

  @override
  Widget build(BuildContext context) {
    if(currencies.isEmpty){
      Navigator.of(context).pop();
    }
    return Scaffold(
      body: Center(
        child: ListView(
          physics: const BouncingScrollPhysics(),
          children: currencies.map((currency) => ListTile(
            title: Text(currency),
            onTap: () {
              Provider.of<CurrentCurrencys>(context, listen: false).add(context, currency);
              Navigator.of(context).pop();
            }
          )).toList()
        ),
      ),
    );
  }
}