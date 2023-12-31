from model import Api
import threading
import view


class Presenter:
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__new__(cls)
        return cls._instances

    def __init__(self, view, *args, **kwargs):
        self.view = view
        self.switch_search = False
        self.switch_NOalchol = False
        self.ingredient = False



    def switch_update(self, switch, _, togle):
        if togle == 1:
            self.switch_search = switch.get_active()
        else:
            self.switch_NOalchol = switch.get_active()
        return switch.get_active()

    def searchButon(self, widget, spinner):
        spinner.start()
        self.ingredient = False
        if self.switch_search == False:
            self.searchCocktails(widget.get_text())
        else:
            self.searchByIngredient(widget.get_text())
        spinner.stop()

    def get_cocktail(self, btn, drkN, drkI, name):
        def cocktailTh(self, name, drkN, drkI):
            if not name:
                self.ingredient = False
                api = Api.get_api_rand()
            else:
                api = Api.get_api_coctail(name)
            if not api == None:
                api = api["drinks"][0]
                img = Api.get_api_img(api["strDrinkThumb"])
                ingredientes = ""
                i = 1
                while (api["strIngredient" + str(i)] != None and i < 16):
                    if not api["strMeasure" + str(i)] == None:
                        ingredientes = ingredientes + api["strIngredient" + str(i)] + "  ->  " + api[
                            "strMeasure" + str(i)] + "\n"
                    else:
                        ingredientes = ingredientes + api["strIngredient" + str(i)] + "\n"
                    i = i + 1
                instructions = [api["strInstructions"], api["strInstructionsES"],
                                api["strInstructionsDE"], api["strInstructionsFR"], api["strInstructionsIT"]]
                view.run_on_main_th(self.view.cocktail, api["strDrink"], ingredientes, instructions, img, drkN, drkI)
            else:
                view.run_on_main_th(self.view.error, [], [])

        th = threading.Thread(target=cocktailTh, args=(self, name, drkN, drkI,))
        th.start()

    def searchCocktails(self, search):

        def cocktailsTh(self, search):
            api = Api.get_api_coctail(search)
            if api == None:
                view.run_on_main_th(self.view.error, [], [])
                return
            else:
                api = api["drinks"]
                drinksNames = []
                drinksImg = []
                if api != None:
                    th = []
                    for cocktail in api:
                        if self.switch_NOalchol == True:
                            if cocktail["strAlcoholic"] != "Alcoholic":
                                drinksNames.append(cocktail["strDrink"])
                                drinksImg.append("")
                                th.append(threading.Thread(target=Presenter.imgGetTh, args=(
                                cocktail["strDrinkThumb"], len(drinksNames) - 1, drinksImg,)))
                                th[len(drinksNames) - 1].start()
                        else:
                            drinksNames.append(cocktail["strDrink"])
                            drinksImg.append("")
                            th.append(threading.Thread(target=Presenter.imgGetTh, args=(
                            cocktail["strDrinkThumb"], len(drinksNames) - 1, drinksImg,)))
                            th[len(drinksNames) - 1].start()

                    for thr in th:
                        thr.join()
                    view.run_on_main_th(self.view.home, "", drinksNames, drinksImg)
                else:
                    view.run_on_main_th(self.view.error, [], [])
                    return

        th = threading.Thread(target=cocktailsTh, args=(self, search,))
        th.start()

    def searchByIngredient(self, search):
        def SByIngredientTh(self, search):
            api = Api.get_api_ingredient(search)
            if api == None:
                view.run_on_main_th(self.view.error, [], [])
                return
            else:
                if api["ingredients"] == None:
                    view.run_on_main_th(self.view.error, [], [])
                    return
                api = api["ingredients"][0]["strIngredient"]
                filteres = Api.get_api_by_ingredient(api)
                if filteres == None:
                    view.run_on_main_th(self.view.error, [], [])
                    return
                else:
                    filteres = filteres["drinks"]
                    drinksNames = []
                    drinksImg = []
                    th = []
                    for cocktail in filteres:
                        if self.switch_NOalchol == True:
                            info = Api.get_api_id_coctail(cocktail["idDrink"])
                            if info != None and info["drinks"][0]["strAlcoholic"] != "Alcoholic":
                                drinksNames.append(cocktail["strDrink"])
                                drinksImg.append("")
                                th.append(threading.Thread(target=Presenter.imgGetTh, args=(
                                cocktail["strDrinkThumb"], len(drinksNames) - 1, drinksImg,)))
                                th[len(drinksNames) - 1].start()
                        else:
                            drinksNames.append(cocktail["strDrink"])
                            drinksImg.append("")
                            th.append(threading.Thread(target=Presenter.imgGetTh, args=(
                            cocktail["strDrinkThumb"], len(drinksNames) - 1, drinksImg,)))
                            th[len(drinksNames) - 1].start()

                    for thr in th:
                        thr.join()
                    view.run_on_main_th(self.view.home, "", drinksNames, drinksImg)

        th = threading.Thread(target=SByIngredientTh, args=(self, search,))
        th.start()

    def get_ingredients(self, _, spinner):
        spinner.start()

        def ingreImgGetTh(name, pos, imgs):
            api = Api.get_ingredient_img(name)
            imgs[pos] = api
            return

        def GETingredientsTh(self):
            api = Api.get_api_Ingredients()
            if api == None:
                view.run_on_main_th(self.view.error, [], [])
                return
            else:

                api = api["drinks"]
                ingredientName = []
                ingredientImg = []
                th = []
                for ingredient in api:
                    ingredientImg.append("")
                    th.append(threading.Thread(target=ingreImgGetTh, args=(
                    ingredient["strIngredient1"], len(ingredientName), ingredientImg,)))
                    th[len(ingredientName)].start()
                    ingredientName.append(ingredient["strIngredient1"])
                for thr in th:
                    thr.join()
                self.ingredient = True
                spinner.stop()
                view.run_on_main_th(self.view.home, "", ingredientName, ingredientImg)

        th = threading.Thread(target=GETingredientsTh, args=(self,))
        th.start()

    def searchIngredi(self, _, name):
        self.ingredient = False
        self.searchByIngredient(name)

    def imgGetTh(url, pos, imgs):
        api = Api.get_api_img(url)
        imgs[pos] = api
        return
