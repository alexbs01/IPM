import 'package:app/view/screens/add_currency.dart';
import 'package:app/view_model/current_currencys.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../../view_model/currencys.dart';
import '../widgets/number_input.dart';
import '../widgets/select_currency.dart';

class HomeTablet extends StatelessWidget{
  const HomeTablet({super.key});

  @override
  Widget build(BuildContext context) {
    Provider.of<Currencys>(context,listen: false).generateCurrencys();
    
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 40, 20, 0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  selectCurrency(context, MediaQuery.of(context).size.width * 0.4, Provider.of<Currencys>(context).currencys),
                  numberInput(context, MediaQuery.of(context).size.width * 0.4),
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 0.4,
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(0, 0, 0, 10),
                      child: Visibility(
                        visible: Provider.of<Currencys>(context).error!="" || Provider.of<CurrentCurrencys>(context).localErr!="",
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(30),
                            color: const Color.fromRGBO(230, 230, 230, 1),
                            gradient: const LinearGradient(
                              begin: Alignment.topCenter,
                              end: Alignment.bottomCenter,
                              colors: [Color.fromARGB(255, 238, 238, 238), Color.fromARGB(255, 226, 226, 226)],
                            ),
                            boxShadow: const [
                              BoxShadow(color: Color.fromRGBO(230, 230, 230, 1), spreadRadius: 1),
                            ],
                          ),
                          child: Padding(
                            padding: const EdgeInsets.fromLTRB(10, 15, 10, 15),
                            child: Column(
                              children: [
                                const Icon(
                                  Icons.wifi,
                                  color: Colors.red,
                                ),
                                Text(Provider.of<Currencys>(context).error!=""?Provider.of<Currencys>(context).error:Provider.of<CurrentCurrencys>(context).localErr, style: const TextStyle(color: Colors.red)),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              Expanded(
                child: _list(context)
              ),
              
              
            ],
          ),
        )
      ),
      floatingActionButton: FloatingActionButton(
          backgroundColor: Provider.of<CurrentCurrencys>(context, listen: false).selected==""?Colors.grey:Colors.blue,
          onPressed: () {
            if(Provider.of<CurrentCurrencys>(context, listen: false).selected!=""){
              Navigator.push(context, MaterialPageRoute(builder: (context) =>
                  AddCurrency(currencies: Provider.of<Currencys>(context).currencys))
              );
            }
          },
          tooltip: 'Add currency',
          child: const Icon(Icons.add)
      ),
    );
  }

  Widget _list(BuildContext context){
  return ListView.builder(
      physics: const BouncingScrollPhysics(),
      itemCount: Provider.of<CurrentCurrencys>(context).exchanges.length,
      itemBuilder: (context, index){
        return _listContainer(context, index);
      },
    );
}

  Widget _listContainer(BuildContext context, int index){
    return LayoutBuilder(builder: (BuildContext context, BoxConstraints constraints){
      var exchange = Provider.of<CurrentCurrencys>(context).exchanges[index];
      var currency = exchange.$1;
      var value = exchange.$2*Provider.of<CurrentCurrencys>(context, listen: true).currentValue;
      var widthContainer = MediaQuery.of(context).size.width * 0.4;
      Color boxColor = const Color.fromRGBO(230, 230, 230, 1);
      return Container(
        margin: const EdgeInsets.fromLTRB(0, 0, 0, 10),
        width: widthContainer,
        height: 90,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(30),
          color: boxColor,
          gradient: const LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color.fromARGB(255, 238, 238, 238), Color.fromARGB(255, 226, 226, 226)],
          ),
          boxShadow: [
            BoxShadow(color: boxColor, spreadRadius: 1),
          ],
        ),
        child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SizedBox(
                width: widthContainer * 0.20,
                child: Center(child: Text(
                  "$currency  ",
                  textAlign: TextAlign.center,
                  textScaleFactor: 2,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                )
              ),

              SizedBox(
                width: widthContainer * 0.60,
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Text(
                    Provider.of<CurrentCurrencys>(context).formatDouble(value),
                    textAlign: TextAlign.center,
                    textScaleFactor: 2,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  )
                )
              ),

              SizedBox(
                width: widthContainer * 0.10,
                child: IconButton(
                    icon: const Icon(Icons.delete_outline),
                    color: const Color.fromARGB(255, 165, 165, 165),
                    onPressed: () {Provider.of<CurrentCurrencys>(context, listen: false).removeExchange(index);},
                  ),
              ),
              
            ],
          )
      );
    });
  }
}