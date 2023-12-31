import gi
import gettext

import locale

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf, GLib
from presenter import Presenter

t = gettext.gettext
# Creamos la clase App, que será la contenedora de la aplicación
class App(Gtk.Application):
    # Cuando creamos un objeto App, lo conectamos con el método on_activate

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.win = None

    def on_activate(self, app):
        if not self.win:
            self.win = View(application=app)
            Presenter(self.win)
        self.win.present()

run_on_main_th = GLib.idle_add
# La clase View, muestra la vista de la Aplicación
class View(Gtk.ApplicationWindow):
    
    # Por defecto muestra home
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.presenter = Presenter(self)
        self.spinner = Gtk.Spinner()
        self.home("",[],[])

    # home, es la vista principal del programa, posee los elementos de búsqueda
    def home(self, _,drinksName, drinksImg, *args, **kwards):
        # =================== ESTABLECEMOS VALORES POR DEFECTO ===================
        self.set_default_size(1300, 600)
        self.set_title("El Bar")
        self.set_resizable(False)  # Obligamos a que no se pueda redimensionar la ventana

        # ================== CREACIÓN DE LOS ELEMENTOS DE LA VISTA ====================
        # -------- CAJA DEL TÍTULO -----------
        title = Gtk.Label()
        title.set_markup("<big><b>El Bar</b></big>")
        title.set_margin_start(20)
        title.set_margin_top(20)
        title.set_margin_bottom(20)

        # Creamos un separador que separe el título del resto de la aplicación
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        # -------- CAJA ELECCIÓN DE COCKTAIL O INGREDIENTE ----------
        cocktail = Gtk.Label()
        cocktail.set_text(t("Cocktail"))

        ingredients = Gtk.Label(label = t("Ingrediente"))
        ingredientButton = Gtk.Button()
        ingredientButton.set_child(ingredients)
        ingredientButton.set_has_frame(False)
        self.spinner = Gtk.Spinner()
        ingredientButton.connect('clicked', Presenter(self).get_ingredients, self.spinner)

        cocktailOrIngredient = Gtk.Switch()
        cocktailOrIngredient.set_active(Presenter(self).switch_search)
        cocktailOrIngredient.set_margin_start(10)
        cocktailOrIngredient.set_margin_end(10)
        cocktailOrIngredient.connect('notify::active', Presenter(self).switch_update, 1)

        # ------------- CAJA DE BUSCADOR Y COCKTAIL ALEATORIO -------------
        # Creamos los inputs y cada uno con sus caracteríscas
        search = Gtk.Entry()
        search.set_placeholder_text(t("Que quieres buscar?"))
        search.set_margin_end(20)
        search.connect('activate', Presenter(self).searchButon, self.spinner)


        randomCocktail = Gtk.Button(label=t("Vamos a probar cosas nuevas"))
        randomCocktail.connect('clicked', Presenter(self).get_cocktail, drinksName, drinksImg, "")

        # ----------- BLOQUE DE FILTRO DE ALCOHOL ------------
        alcohol = Gtk.Label()
        alcohol.set_text(t("No alcoholic"))

        alcocholOrNot = Gtk.Switch()
        alcocholOrNot.set_active(Presenter(self).switch_NOalchol)
        alcocholOrNot.connect('notify::active', Presenter(self).switch_update, 2)

        # ======================= RESULTADOS DE BÚSQUEDA =======================
        # Lista de cockteles
        scrollBar = Gtk.ScrolledWindow()  # Creamos un scrollbar por si en el resultado hay muchos cócteles

        grid = Gtk.Grid()  # Y creamos un grid para controlar de que forma aparecerán listados
        grid.set_column_homogeneous(True)
        grid.set_margin_start(20)
        grid.set_margin_end(20)
        grid.set_margin_bottom(20)
        grid.set_row_spacing(30)

        max_columns = 5  # Establecemos que habrá un máximo de 5 columnas en el grid
        row, col = 0, 0

        # Recorresmos los arrays pasados por parámetros
        for name, image in zip(drinksName, drinksImg):

            if image != None:  # Si no hay imagen es que no hay cócteles, porque todos los cócteles tienen imagen
                # Creamos una caja vertical para meter dentro la imagen y el nombre
                vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)


                # Cargamos la imagen y la redimensionamos
                pbuf = GdkPixbuf.PixbufLoader()
                pbuf.write(image)
                pbuf.close()

                cocktailImage = Gtk.Image()
                cocktailImage.set_from_pixbuf(pbuf.get_pixbuf())
                cocktailImage.set_pixel_size(self.get_default_size()[0] * 0.178)

                button = Gtk.Button()
                button.set_has_frame(False)
                button.set_child(cocktailImage)
                if Presenter(self).ingredient:
                    button.connect('clicked', Presenter(self).searchIngredi, name)
                else: 
                    button.connect('clicked', Presenter(self).get_cocktail, drinksName, drinksImg, name)
            else:
                break

            drinkName = Gtk.Label(label = name)  # Creamos la etiqueta con el nombre
            drinkName.set_natural_wrap_mode(True)
            drinkName.set_wrap(True)
            # Insertamos en la caja la imagen y el nombre
            vBox.append(button)
            vBox.append(drinkName)


            # Insertamos la caja en el grid
            grid.attach(vBox, col, row, 1, 1)

            col += 1  # Calculamos cual será la próxima posición a rellenar en el grid

            if col >= max_columns:
                col = 0
                row += 1

        # Cuando esté el grid formado, lo incorporamos al scrollbar
        scrollBar.set_child(grid)
        scrollBar.set_propagate_natural_width(True)
        scrollBar.set_min_content_height(400)

        # ------------- CAJA CON IMAGEN E INSTRUCCIONES ---------------
        if not drinksImg:
            mainImg = Gtk.Image()
            mainImg.set_from_file("../cocktailGirl.png")
            mainImg.set_pixel_size(self.get_default_size()[0] * 0.25)
            mainImg.set_margin_start(20)
            mainImg.set_margin_bottom(20)

        # ================= CREAMOS CAJAS E INCORPORAMOS TOD0 A CADA UNA DE ELLAS ===================
        # ------------ CAJA PRINCIPAL, ALINEADO VERTICAL ------------
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # ------------ CAJA DEL TÍTULO -------------
        boxTitle = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxTitle.append(title)

        # ------------ CAJA DE COCKTAIL O INGREDIENTE---------
        boxCocktailIngredient = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxCocktailIngredient.append(cocktail)
        boxCocktailIngredient.append(cocktailOrIngredient)
        boxCocktailIngredient.append(ingredientButton)
        boxCocktailIngredient.append(self.spinner)
        boxCocktailIngredient.set_halign(Gtk.Align.CENTER)
        boxCocktailIngredient.set_margin_top(20)
        boxCocktailIngredient.set_margin_bottom(20)

        # ------------ CAJA DEL BUSCADO Y EL BOTÓN DE ALEATORIO -------------
        boxSearchRandomSearch = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxSearchRandomSearch.append(search)
        boxSearchRandomSearch.append(randomCocktail)
        boxSearchRandomSearch.set_halign(Gtk.Align.CENTER)
        boxSearchRandomSearch.set_margin_bottom(20)

        # ------------ CAJA DEL SELECTOR DE ALCOHOL -----------
        boxSwitchAlcohol = Gtk.Box()
        boxSwitchAlcohol.append(alcocholOrNot)
        boxSwitchAlcohol.set_halign(Gtk.Align.CENTER)

        boxAlcohol = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxAlcohol.append(alcohol)
        boxAlcohol.set_halign(Gtk.Align.CENTER)
        boxAlcohol.set_margin_bottom(20)

        boxAlcohol.append(boxSwitchAlcohol)

        # ------------ CAJA DEL RESULTADO DE BÚSQUEDA -----------

        if drinksName and drinksImg:
            boxList = Gtk.Box()
            boxList.append(scrollBar)
        elif not drinksImg:

            instructionsTitle = Gtk.Label()
            instructionsTitle.set_markup(t("<big><b>Instrucciones</b></big>"))
            instructionsTitle.set_margin_top(20)
            instructionsTitle.set_margin_bottom(20)
            instructionsTitle.set_margin_end(20)

            instructionsText = t("""Yendo de arriba a abajo y de izquierda a derecha:
            1- El Switch de selección de cócteles o ingredientes, permite indicar que se va a buscar
            2- En el Buscador se debe escribir que buscar
            3- El botón de la derecha del buscador, elegirá un cóctel aleatorio y lo mostrará para probar cosas nuevas
            4- En el último Switch, por defecto se buscarán cócteles con alcohol y sin él, pero cuando se use por primera vez,
                mostrará o sólo las alcohólicas o las no alcohólicas""")
            instructions = Gtk.Label(label = instructionsText)
            instructions.set_natural_wrap_mode(True)
            instructions.set_wrap(True)
            instructions.set_margin_end(40)

            boxInitial = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
            boxInitial.set_homogeneous(True)

            boxImage = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
            boxImage.append(mainImg)

            boxInstructions = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
            boxInstructions.append(instructionsTitle)
            boxInstructions.append(instructions)

            boxInitial.append(boxImage)
            boxInitial.append(boxInstructions)


        # ------------ INCOROPORAMOS CADA CAJA A LA PRINCIPAL -----------
        mainBox.append(boxTitle)
        mainBox.append(separator)
        mainBox.append(boxCocktailIngredient)
        mainBox.append(boxSearchRandomSearch)
        mainBox.append(boxAlcohol)
        if drinksName and drinksImg:
            mainBox.append(boxList)
        elif not drinksImg:
            mainBox.append(boxInitial)


        # Establecemos la etiqueta como hija de la ventana
        self.set_child(mainBox)

    def cocktail(self, name, ingredients, instructions, image, drkN, drkI, *args, **kwargs):
        # =================== ESTABLECEMOS VALORES POR DEFECTO ===================
        self.set_default_size(1300, 600)
        self.set_title("El Bar")
        self.set_resizable(False)  # Obligamos a que no se pueda redimensionar la ventana
        # ================== CREACIÓN DE LOS ELEMENTOS DE LA VISTA ====================
        # -------- CAJA DEL TÍTULO -----------
        # Creamos etiquetas que aparecerán en el buscador, y cada una con sus características
        title = Gtk.Label()
        title.set_markup("<big><b>El Bar</b></big>")
        title.set_margin_start(20)
        title.set_margin_top(20)
        title.set_margin_bottom(20)

        goBack = Gtk.Button(label=" < ")
        goBack.set_margin_end(20)
        goBack.connect('clicked', self.home, drkN, drkI)

        # ------------------ SEPARADOR -----------------
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_bottom(20)

        # ----------------- BLOQUE DEL TÍTULO E IMAGEN ------------------
        # Creación de la etiqueta con el nombre
        cocktailName = Gtk.Label()
        cocktailName.set_margin_bottom(20)
        cocktailName.set_markup(t(f"<big><b>{name}</b></big>"))

        # Creación de la imagen
        cocktailImage = Gtk.Image()
        if image != None:
            pbuf = GdkPixbuf.PixbufLoader()
            pbuf.write(image)
            pbuf.close()
            cocktailImage.set_from_pixbuf(pbuf.get_pixbuf())
            cocktailImage.set_pixel_size(self.get_default_size()[0] * 0.35)

        # ------------------- BLOQUE DE INSTRUCCIONES PARA PREPARACIÓN -------------------
        # Etiqueta con el nombre del bloque
        preparation = Gtk.Label()
        preparation.set_markup(t("<big><b>Preparation</b></big>"))
        preparation.set_margin_bottom(20)

        # Etiqueta que contendrá la preparación

        if locale.getlocale()[0] == "es_ES":
            instructionsA = instructions[1]
        elif locale.getlocale()[0] == "de_DE":
            instructionsA = instructions[2]
        elif locale.getlocale()[0] == "fr_FR":
            instructionsA = instructions[3]
        elif locale.getlocale()[0] == "it_IT":
            instructionsA = instructions[4]
        else:
            instructionsA = instructions[0]

        if instructionsA == None:
            instructionsA = instructions[0]

        instructionsCocktail = Gtk.Label(label = instructionsA)
        instructionsCocktail.set_natural_wrap_mode(True)
        instructionsCocktail.set_wrap(True)
        instructionsCocktail.set_margin_start(20)
        instructionsCocktail.set_margin_end(20)
        instructionsCocktail.set_yalign(Gtk.Align.FILL)

        # Creamos un scrollbar por si las intrucciones de la preparación son muy largas
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(instructionsCocktail)
        scrolled.set_propagate_natural_width(True)
        scrolled.set_min_content_height(400)

        # ---------------- BLOQUE DE LA LISTA DE INGREDIENTES -----------------
        # Etiqueta del nombre del bloque
        ingredientsLabel = Gtk.Label()
        ingredientsLabel.set_markup(t("<big><b>Ingredientes</b></big>"))
        ingredientsLabel.set_margin_bottom(20)

        # Lista de ingredientes
        ingredientsList = Gtk.Label()
        ingredientsList.set_text(ingredients)
        ingredientsList.set_wrap(True)
        ingredientsList.set_natural_wrap_mode(True)
        ingredientsList.set_margin_start(20)
        ingredientsList.set_margin_end(20)

        # ====================== CREACIÓN DE LAS CAJAS ====================
        # ---------------- CAJAS PRINCIPALES HORIZONTAL Y VERTICAL ---------------
        # La horizontal principal contendrá las tres cajas verticales de los datos del cocktail
        mainBoxH = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mainBoxH.set_homogeneous(True)
        mainBoxH.set_baseline_position(Gtk.BaselinePosition.BOTTOM)

        # La vertical principal contedrá la estructura general de la vista
        mainBoxV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # ---------------- CAJA DEL TITULO -----------------
        boxTitle = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxTitle.append(title)
        boxTitle.append(goBack)

        # -------------- CAJA DEL NOMBRE Y LA FOTO DEL COCKTAIL ------------------
        boxNameImage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxNameImage.append(cocktailName)
        boxNameImage.append(cocktailImage)
        boxNameImage.set_halign(Gtk.Align.CENTER)
        boxNameImage.set_margin_start(20)
        boxNameImage.set_margin_bottom(20)

        # -------------- CAJA CON LA PREPARACIÓN DEL COCKTAIL -----------------
        boxPreparation = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxPreparation.set_halign(Gtk.Align.CENTER)
        boxPreparation.append(preparation)
        boxPreparation.append(scrolled)

        # -------------- CAJA CON LA LISTA DE INGREDIENTES -----------------
        boxIngredients = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxIngredients.set_halign(Gtk.Align.CENTER)
        boxIngredients.append(ingredientsLabel)
        boxIngredients.append(ingredientsList)

        # Estas tres últimas cajas las insertamos dentro de la principal horizontal
        mainBoxH.append(boxNameImage)
        mainBoxH.append(boxPreparation)
        mainBoxH.append(boxIngredients)

        # Y en la principal vertical, estructuramos finalmente la aplicación
        mainBoxV.append(boxTitle)
        mainBoxV.append(separator)
        mainBoxV.append(mainBoxH)

        # Establecemos la etiqueta como hija de la ventana
        self.set_child(mainBoxV)

    def error(self, drkN, drkI):
        # =================== ESTABLECEMOS VALORES POR DEFECTO ===================
        self.set_default_size(1300, 644)
        self.set_title("El Bar")
        self.set_resizable(False)  # Obligamos a que no se pueda redimensionar la ventana

        # ============ CREAMOS ETIQUETA Y BOTÓN ==============
        errorLabel = Gtk.Label()
        errorLabel.set_markup(t("<big><b>El cocktail no se encontró o no se pudo conectar al servidor</b></big>"))
        errorLabel.set_margin_bottom(20)

        closeWindowButton = Gtk.Button(label=t("Volver al buscador"))
        closeWindowButton.connect('clicked', self.home, drkN, drkI)  # Asignamos la acción de cerrar ventana al botón

        # =========== CREAMOS UN CAJA VERTICAL PRINCIPAL ============
        errorBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        errorBox.set_halign(Gtk.Align.CENTER)
        errorBox.set_valign(Gtk.Align.CENTER)

        # ---------- ASOCIAMOS LOS ELEMENTOS A LA CAJA ------------
        errorBox.append(errorLabel)
        errorBox.append(closeWindowButton)

        self.set_child(errorBox)

