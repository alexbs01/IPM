import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../view_model/current_currencys.dart';

Widget selectCurrency(BuildContext context, double size, List<String> currencys){
  return Container(
      key: const ValueKey('dropdownSelectCurrency'),
      width: size,
      alignment: Alignment.center,
      child: DropdownButtonFormField(
        onChanged: (value) {Provider.of<CurrentCurrencys>(context, listen: false).updateExchanges(context, value??"");},
        isDense: true,
        isExpanded: true,
        hint: const Text("Select a currency"),
        decoration: const InputDecoration(
          filled: true,
          fillColor: Color.fromARGB(255, 240, 240, 240),
        ),
        items: currencys.map((e) {
          return DropdownMenuItem(
            value: e,
            child: SizedBox(
              width: double.infinity,
              child: Text(
                e,
                overflow: TextOverflow.ellipsis,
              ),
            ),
          );
        }).toList(),
      )
  );
}