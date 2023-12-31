import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../../view_model/current_currencys.dart';

Widget numberInput(BuildContext context, double size) {
  return Container(
    width: size,
    height: 90,
    alignment: Alignment.center,
    child: TextFormField(
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      inputFormatters: [FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d{0,2}'))],
      onChanged: (String value){
        Provider.of<CurrentCurrencys>(context, listen: false).currentValue = double.parse(value==""?"0":value);
      },
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'Valor',
      ),
    ),
  );
}