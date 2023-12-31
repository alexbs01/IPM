import 'package:app/view_model/currencys.dart';
import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import '../model/model.dart';

class CurrentCurrencys extends ChangeNotifier{
  List<(String, double)> _exchanges = [];
  String selected = "";
  double _currentValue = 0;
  String localErr = "";

  double get currentValue => _currentValue;

  set currentValue(double value) {
    _currentValue = value;
    notifyListeners();
  }

  List<(String, double)> get exchanges => _exchanges;

  Future<void> updateExchanges(BuildContext context, String selected) async {
    this.selected = selected;
    String symbol = "";

    if(_exchanges.isEmpty){
      notifyListeners();
      return;
    }

    for (var i = 0; i<_exchanges.length; i++){
      symbol = "$symbol${this.selected}/${_exchanges[i].$1},";
    }
    symbol = symbol.substring(0, symbol.length-1);

    var response = (await Model().getRate(symbol));
    var exch = response.$1;
    if(response.$2!=""){
      Provider.of<Currencys>(context, listen: false).error=response.$2;
      notifyListeners();
      return;
    }else {
      Provider.of<Currencys>(context, listen: false).error="";
    }

    for (var i = 0; i<exch.length; i++) {
      _exchanges[i] = (_exchanges[i].$1, exch[i]);
    }
    notifyListeners();
  }
  void removeExchange(int index){
    _exchanges.removeAt(index);
    notifyListeners();
  }


  Future<void> add(BuildContext context, String currency) async {
    if(selected!=currency) {
      var response = await Model().getRate("$selected/$currency");
      if(response.$2!=""){
        localErr=response.$2;
        notifyListeners();
        return;
      }else {
        localErr="";
      }
      _exchanges.add((currency, response.$1.first));
    }
    notifyListeners();
  }

  String formatDouble(double value){
    var formatting = (value).toString().split('.');
    for (var i = formatting[1].length; i<2; i++){
      formatting[1] += "0";
    }
    return "${formatting[0]}.${formatting[1].substring(0, 2)}";
  }
}