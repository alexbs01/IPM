import sys
import gettext
import locale

from view import App

try:
    locale.setlocale(locale.LC_ALL, '')

except locale.Error:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

locale_dir = "locale"
locale.bindtextdomain("ipm-2324-p1-grupo_71", locale_dir)

gettext.bindtextdomain("ipm-2324-p1-grupo_71", locale_dir)
gettext.textdomain("ipm-2324-p1-grupo_71")

app = App()
app.run(sys.argv)
