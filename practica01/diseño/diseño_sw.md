# Diseño software
Haremos uso en esta practica del patrón MVP
## Diagrama de estados
```mermaid
stateDiagram-v2
	[*] --> Inicio
	Inicio --> Buscar_cóctel

	Buscar_cóctel --> Buscar_por_alcóholica

	Buscar_cóctel --> Buscar_por_ingrediente

	state if_state <<choice>>
	Buscar_por_alcóholica --> if_state
	Buscar_por_ingrediente --> if_state

	if_state --> Ver_resultados_búsqueda: Búsqueda correcta
	if_state --> Ver_ventana_error: Búsqueda incorrecta
    
    state join_state <<join>>
	Ver_ventana_error --> join_state
	Ver_resultados_búsqueda --> Se_elige_algún_resultado?
	
	Se_elige_algún_resultado? --> Ver_cóctel: Si se elige otro
	Se_elige_algún_resultado? --> join_state: No se elige otro
	Ver_cóctel --> join_state
	
	state if_state2 <<choice>>
	join_state --> if_state2
	if_state2 --> Inicio: Se busca otro cóctel
	if_state2 --> [*]: No se busca otro cóctel
```
## Diagrama de secuencia
### Buscar cocktel
```mermaid
sequenceDiagram
	participant App
	participant View
	participant Presenter
	participant Model
	
	App->>+App: __init__(kwargs)
		App->>+View: on_activate(app)
		
			View->>+Presenter: __init__(args, kwargs)
				Presenter->>Presenter: __init__(cview)
			Presenter-->>-View: return
				
			View->>+View: home()
				View->>+Presenter: switch_update(togle)
				Presenter-->>-View: return
				
				View->>+Presenter: searchButon()
					Presenter->>+Presenter: searchCocktails(name)
						Presenter->>+Presenter: cocktailsTh(name) {ejecución concurrente}
							Presenter->>+Model: get_api_cocktail(name)
								Model->>+Model: get_api_data(url)
								Model-->>-Model: return
							Model-->>-Presenter: return
							loop getCoctails
								Presenter->>+Presenter: imgGetTh(url, pos, imgs) {ejecución concurrente}
									Presenter->>+Model: get_api_img(url)
									Model-->>-Presenter: return
								Presenter->>-Presenter: return
							end
						Presenter->>-Presenter: return
					Presenter-->>-Presenter: return
				Presenter-->>-View: return
				View->>+Presenter: get_cocktail(name)
					Presenter->>+Presenter: cocktailTh(name) {ejecución concurrente}
						Presenter->>+Model: get_api_cocktail(name)
							Model->>+Model: get_api_data(url)
							Model-->>-Model: return
						Model-->>-Presenter: return
						Presenter->>+Model: get_api_img(url)
						Model-->>-Presenter: return
						Presenter->>+View: cocktail(name, imgredientes, img)
						View-->>-Presenter: return
					Presenter->>-Presenter: return
				Presenter-->>-View: return
			View-->>-View: return
		
	View-->>-App: return
```
### Buscar ingrediente 
```mermaid
sequenceDiagram
	participant App
	participant View
	participant Presenter
	participant Model
	
	App->>+App: __init__(kwargs)
		App->>+View: on_activate(app)
	
			View->>+Presenter: __init__(args, kwargs)
				Presenter->>Presenter: __init__(cview)
			Presenter-->>-View: return
	
			View->>+View: home()
				View->>+Presenter: switch_update(togle)
				Presenter-->>-View: return
	
			View->>+Presenter: searchButon()
				Presenter->>+Presenter: searchByIngredient(name)
					Presenter->>+Presenter: searchByIngridientTh(name) {ejecución concurrente}
						Presenter->>+Model: get_api_ingredients(name)
						Model-->>-Presenter: return
						Presenter->>+Model: get_api_by_ingredients()
						Model-->>-Presenter:return
						loop getCoctails
							Presenter->>+Presenter: imgGetTh(url, pos, imgs) {ejecución concurrente}
								Presenter->>+Model: get_api_img(url)
								Model-->>-Presenter: return
							Presenter->>-Presenter: return
						end
					Presenter->>-Presenter: sreturn
				Presenter-->>-Presenter: return
			Presenter-->>-View: return
			View->>+Presenter: get_cocktail(name)
				Presenter->>+Presenter: cocktailTh(name) {ejecución concurrente}
					Presenter->>+Model: get_api_cocktail(name)
						Model->>+Model: get_api_data(url)
						Model-->>-Model: return
					Model-->>-Presenter: return
					Presenter->>+Model: get_api_img(url)
					Model-->>-Presenter: return
					Presenter->>+View: cocktail(name, imgredientes, img)
					View-->>-Presenter: return
				Presenter->>-Presenter: return
			Presenter-->>-View: return
		View-->>-View: return
	
	View-->>-App: return
```
### Cocktel aleatorio
```mermaid
sequenceDiagram
	participant App
	participant View
	participant Presenter
	participant Model
	
	App->>+App: __init__(kwargs)
		App->>+View: on_activate(app)
	
			View->>+Presenter: __init__(args, kwargs)
				Presenter->>Presenter: __init__(cview)
			Presenter-->>-View: return
	
			View->>+View: home()
				View->>+Presenter: switch_update(togle)
				Presenter-->>-View: return
	
			View->>+Presenter: get_cocktail(name)
				Presenter->>+Presenter: cocktailTh(name) {ejecución concurrente}
					Presenter->>+Model: get_api_rand()
						Model->>+Model: get_api_data(url)
						Model-->>-Model: return
					Model-->>-Presenter: return
					Presenter->>+Model: get_api_img(url)
					Model-->>-Presenter: return
					Presenter->>+View: cocktail(name, imgredientes, img)
					View-->>-Presenter: return
				Presenter->>-Presenter: return
			Presenter-->>-View: return
		View-->>-View: return
	
	View-->>-App: return
```
## Diagrama de clases
```mermaid
classDiagram
    class Model{
        + str listIngredients
        + str searchCocktail
        + str searchByID
        + str searchIngredient
        + str searchByIngredient
        + str getRandom

        + get_api_data()
        + get_api_rand()
        + get_api_coctail()   
        + get_api_ingredient()
        + get_api_by_ingredients()
        + get_api_id_coctail()
        + get_api_ingredients()
        + get_api_img()
        + get_ingredient_img()
    }

    class App{
        + View win

        - __init__()
        + on_activate() 
    }

    class View{
        + Presenter presenter
        + Gtk.Spinner spinner

        - __init__()
        + home()
        + cocktail()
        + error()
    }
    class Presenter{
        + View view 
        + bool switch_search 
        + bool switch_NOalchol
	+ bool ingredient

        - __new__()
        - __init__()
        + switch_update()
        + serachButom()
        + get_cocktail()
        + searchCocktails()
        + searchByIngredient()
        + get_ingredients()
	+ searchIngredi()
	+ imgGetTh()
    }

    App --> Presenter: creates
    App --> View: creates
    View --> Presenter: uses
    View <-- Presenter
    Presenter --> Model: uses
```
