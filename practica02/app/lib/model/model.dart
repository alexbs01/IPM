import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'dart:async';
import '../server_stub.dart' as stub;

class Model{
  final String _getUrl = "https://fcsapi.com/api-v3/forex/list?type=forex";
  final String _exchangeUrl = "https://fcsapi.com/api-v3/forex/latest?symbol=";
  final String _key = "&access_key=xrsVIOmAqerg9tqGow4oeGb";

  Future<List<String>> getCurrencys() async {
    String error = "";
    List<String> exchangeList = [];

    try {
      final response = await stub.get(Uri.parse(_getUrl + _key));

      if (response.statusCode==200){

        var body = jsonDecode(response.body);
        if(body['msg']=="Successfully") {
          String currency;

          for (var element in (body['response'] as List<dynamic>)) {
            currency = element['symbol'].toString().substring(0,3);

            if (exchangeList.isEmpty){
              exchangeList.add(currency);
            }
            if (exchangeList.last!=currency && exchangeList.firstWhere((element) => element==currency, orElse: ()=>"")==""){
              exchangeList.add(currency);
            }
          }
        }else{
          error = body['msg'];
        }
      }else {
        error = response.statusCode.toString();
      }
    }on SocketException{
      error = "Bad connection";
    }
    if(error!="") exchangeList.add(error);
    return exchangeList;
  }

  Future<(List<double>, String)> getRate(String synchange) async {
    String error = "";
    List<double> respon = [];
    try {
      final response = await stub.get(
          Uri.parse(_exchangeUrl + synchange + _key));
      if (response.statusCode == 200) {
        var body = jsonDecode(response.body);
        if (body['msg'] == "Successfully") {
          for (var element in (body['response'] as List<dynamic>)) {
            respon.add(double.parse(element['c'].toString()));
          }
        }else{
          error = body['msg'];
        }
      }
    }on SocketException{
      error = "Bad connection";
    }
    return (respon, error);
  }
}