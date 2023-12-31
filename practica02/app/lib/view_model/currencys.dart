import 'package:app/model/model.dart';
import 'package:flutter/material.dart';

class Currencys extends ChangeNotifier{
  List<String> _currencys = [];
  String error = "";
  bool _first = false;

  List<String> get currencys => _currencys;

  void generateCurrencys() async {
    if (!_first) {
      Model().getCurrencys().then((value) {
        if (value.length!=1){
          _first=true;
          error = "";
          _currencys=value;
        }else {
          error=value.first;
        }
        notifyListeners();
      });
    }
  }
}