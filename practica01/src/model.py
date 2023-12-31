import requests

class Api:
    listIngredients = "list.php?i=list"
    searchCocktail = "search.php?s="
    searchByID = "lookup.php?i="
    searchIngredient = "search.php?i="
    searchByIngredient = "filter.php?i="
    getRandom = "random.php"

    def get_api_data(data):
        # URL base, con el parámetro "data" se indica que queremos de retorno
        url = "https://www.thecocktaildb.com/api/json/v1/1/" + data

        try:
            # Comprobamos que haya conexión con la URL
            response = requests.get(url)

            # Si la hay, retornará el código de error 200, en este caso recibiremos el json
            if response.status_code == 200:
                data_json = response.json()
                return data_json

            # Si no se puede conectar con la API, retornará el código de error
            else:
                print(f"Error en la solicitud a la API: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud a la API: {str(e)}")
            return None

    def get_api_rand():
        return Api.get_api_data(Api.getRandom)
    def get_api_coctail(search):
        return Api.get_api_data(Api.searchCocktail+search)
    def get_api_ingredient(search):
        return Api.get_api_data(Api.searchIngredient+search)
    def get_api_by_ingredient(ingredient):
        return Api.get_api_data(Api.searchByIngredient+ingredient)
    def get_api_id_coctail(ID):
        return Api.get_api_data(Api.searchByID + ID)
    def get_api_Ingredients():
        return Api.get_api_data(Api.listIngredients)

    def get_api_img(url):
        try:
            img = requests.get(url)

            if img.status_code == 200:
                return img.content
            else:
                print("Not found")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud a la API: {str(e)}")
            return None

    def get_ingredient_img(ingredient):
        url = "https://www.thecocktaildb.com/images/ingredients/" + ingredient + "-Medium.png"
        try:
            img = requests.get(url)
            if img.status_code == 200:
                return img.content
            else:
                print("not found")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud a la API: {str(e)}")
            return None
