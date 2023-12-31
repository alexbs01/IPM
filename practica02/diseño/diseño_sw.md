# Diseño software
En esta práctica haremos uso del patrón MVVM que a diferencia del MVP hace uso de un binder el cual en este caso será la librería provider de flutter.
## Diagrama de clases
```mermaid
classDiagram
		
	App ..> HomeTablet: create
	App ..> HomeMobile: create

	HomeTablet ..> AddCurrencys: create
	HomeMobile ..> AddCurrencys: create

	HomeTablet ..> Currencys: use
	HomeTablet ..> CurrentCurrencys: use
	HomeMobile ..> Currencys: use
	HomeMobile ..> CurrentCurrencys: use

	AddCurrencys ..> Currencys: use
	AddCurrencys ..> CurrentCurrencys: use
	Currencys --> Model
	CurrentCurrencys --> Model
	
	class App{
		+ build(): Widget
	}
	class HomeTablet{
		+ build(): Widget
		- _selectCurrency(): Widget
		- _numberInput(): Widget
		- _list(): Widget
		- _listContainer(): Widget
	}
	class HomeMobile{
		+ build(): Widget
		- _selectCurrency(): Widget
		- _numberInput(): Widget
		- _list(): Widget
		- _listContainer(): Widget
	}
	class AddCurrencys{
		+ build(): Widget
		- _add(): void
		- _denay(): void
	}
	class Currencys{
		- List~String~ _currencys
		+ String error
		- bool _first
		+ getCurrencys(): List~String~
		+ generateCurrencys(): void
	}
	class CurrentCurrencys{
		- List< (String, double) > _exchanges
		+ String selected
		+ String localError
		+ double currentValue
		+ getExchanges(): List< (String, double) >
		+ add(): void
		+ removeExchange(): void
		+ formatDouble(): String
		+ updateExchanges(): Future~void~
	}
	class Model{
		- String _getUtl
		- String _exchangeUtl
		- String _key
		+ getRate(): Future< List< (String, double) > >
		+ getCurrencys(): Future< List~String~ >
	}
```
## Diagrama secuencia
Usaremos Home como representación de HomeMobile y HomeTablet ya que funcionalmente son los mismo.
### Añadir moneda
```mermaid
sequenceDiagram
	Home->>+AddCurrencys: Navigator.push()

		AddCurrencys->>+AddCurrencys: _add()
			AddCurrencys->>+CurrentCurrencys: add()
				CurrentCurrencys->>+Model: getRate()
				Model->>-CurrentCurrencys: return
			CurrentCurrencys->>-AddCurrencys: return
		AddCurrencys->>-AddCurrencys: return
	AddCurrencys->>-Home: Navigatro.pop()
```
### Eliminar moneda
```mermaid
sequenceDiagram
	Home->>+CurrentCurrencys: removeExchange()
	CurrentCurrencys->>-Home: return
```
