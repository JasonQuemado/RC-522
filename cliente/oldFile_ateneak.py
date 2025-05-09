import gi
import requests
#Para poder hacer que solo nos de el timetable a partir del dia y hora actual
from datetime import datetime
import threading
import json
import rfid_rc522
#Me faltaba este para poder aplicar el css bien que se me habñia olvidado
import os
import RPi.GPIO as GPIO
from gi.repository import Gtk, Gdk, GLib

gi.require_version("Gtk", "3.0")

SERVER_URL = "http://localhost:55555"

class CourseManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Visualizador Atenea")
        self.set_default_size(800, 500)
        self.set_border_width(10)
        self.rfid = rfid_rc522.Rfid()

        #Cargamos el archivo CSS, la funcion esta abajo
        self.load_css()

        self.logged_in = False
        self.student_name = ""
        self.student_id = ""

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.layout)

        self.loginScreen()

    def load_css(self):
        try:
            #Aqui invocamos al archivo css, no se hace desde un import
            css_path = os.path.abspath("cssGraphic.css")
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            print(f"CSS cargado correctamente desde: {css_path}")
        except Exception as e:
            print(f"Error cargando CSS: {e}")

    def limpiarLayout(self):
        for widget in self.layout.get_children():
            self.layout.remove(widget)

    def loginScreen(self):
        self.limpiarLayout()

        #Esto es para poder dentrar el botón y que no ocupe toda la Layout que es lo que me pasaba
        botonLoginCentrado = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        botonLoginCentrado.set_valign(Gtk.Align.CENTER)
        botonLoginCentrado.set_halign(Gtk.Align.CENTER)

        self.botonLogin = Gtk.Button()
        botonLoginShow = Gtk.Label()
        botonLoginShow.set_justify(Gtk.Justification.CENTER)
        botonLoginShow.set_markup("<span>Please, log in with your university card</span>")
        self.botonLogin.add(botonLoginShow)
        self.botonLogin.set_name("main-button")
        self.botonLogin.set_size_request(400, 150)

        botonLoginCentrado.pack_start(self.botonLogin, False, False, 0)
        self.layout.pack_start(botonLoginCentrado, True, True, 0)

        self.show_all()

        #GLib.idle_add(self.lectorTarjeta)
        #Probamos a ver si no se nos queda colgado
        threading.Thread(target=self.lectorTarjeta, daemon=True).start()

    def lectorTarjeta(self):
        #Invocamos la clase que creamos en el puzzle 1
        try:
            #Añado cosas porque me tarda en leer la tarjeta
            print("Leyendo tarjeta")
            uid = self.rfid.read_uid()
            print("Tarjeta leída")
            if uid:
                GLib.idle_add(self.tarjetaLeida, uid)
            else:
                GLib.idle_add(self.mostrar_error)
        except Exception as e:
            print(f"Error: {e}")
            GLib.idle_add(self.mostrar_error)

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CLOSE, "Access denied")
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def mostrar_error(self):
        self.show_error_dialog("No se ha podido leer la tarjeta.")

    def tarjetaLeida(self, uid):
        try:
            response = requests.get(f"{SERVER_URL}/students?student_id={uid}")
            #Esto significa que la respuesta se ha llevado a cabo con existo(es como que 404 es error, de eso vienen los números)
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.studentName = data[0]["name"]
                    self.studentSurname = data[0]["surname"]
                    #Guardamos bien el id
                    self.studentId = data[0]["student_id"]
                    self.userAuthIn = True
                    self.queryScreen()
                else:
                    self.show_error_dialog("UID no registrado.")
            else:
                self.show_error_dialog("Error del servidor.")
        except Exception as e:
            self.show_error_dialog(f"Error: {e}")

    def queryScreen(self):
        self.limpiarLayout()

        #Aqui ponemos el welcome con los parámetros que hemos guardado antes
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mensajeWelcome = Gtk.Label(label=f"Welcome ")
        mensajeNombre = Gtk.Label()
        surnameName = f"{self.studentSurname} {self.studentName}"
        mensajeNombre.set_markup(f"<span foreground='blue'><b>{surnameName}</b></span>")
        header.pack_start(mensajeWelcome, False, False, 5)
        header.pack_start(mensajeNombre, False, False, 0)

        #Aquí ponemos el botón de logout y utilizamos la función lambda para no tener que hacer una función de nuevo y llamarla cada vez. En SAD hemos hecho algo parecido.
        botonLogout = Gtk.Button(label="Logout")
        botonLogout.connect("clicked", lambda x: self.loginScreen())
        header.pack_end(botonLogout, False, False, 0)

        self.query_entry = Gtk.Entry()
        self.query_entry.set_placeholder_text("enter your query")
        self.query_entry.connect("activate", self.consultaServidor)

        self.result_label = Gtk.Label()
        self.result_label.set_markup("<b></b>")

        self.result_grid = Gtk.Grid()
        self.result_grid.set_column_spacing(10)
        self.result_grid.set_row_spacing(5)
        #CSS
        self.result_grid.set_name("result-grid")

        #Para que ocupe toda la pantalla la tabla utilizamos la funcion ScrolledWindow
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.result_grid)

        self.layout.pack_start(header, False, False, 0)
        self.layout.pack_start(self.query_entry, False, False, 0)
        self.layout.pack_start(self.result_label, False, False, 5)
        self.layout.pack_start(scroll, True, True, 5)

        self.show_all()

	#No nos daba bien asi que lo cambiamos
    #Pero al final solo habia que añadir dos cosas
    #def on_query_entered(self, entry):
        #query = entry.get_text()
        #threading.Thread(target=self.fetch_query_result, args=(query,), daemon=True).start()

    def consultaServidor(self, entry):
        #Recogemos el texto que se haya introducido
        texto = entry.get_text().strip()

        #Si es timetables calculamos el día y hora actual
        if texto == "timetables":
            texto = f"timetables?student_id={self.studentId}"
        elif texto == "students":
			#break
            pass
        elif "?" in texto:
            texto += f"&student_id={self.studentId}"
        else:
            texto += f"?student_id={self.studentId}"

        def peticion():
            try:
                respuesta = requests.get(f"{SERVER_URL}/{texto}")
                if respuesta.status_code == 200:
                    datos = respuesta.json()
                    GLib.idle_add(self.display_results, texto, datos)
                else:
                    print("Error en la petición")
            except Exception as error:
                print(f"Error: {error}")

        #Lanzamos la función peticion en segundo plano
        threading.Thread(target=peticion, daemon=True).start()

    def display_results(self, query, data):
		#Modificamos como se ve la tabla
        #query = query.split("?")[0]
        #self.result_label.set_markup(f"<span foreground='red'><b>{query}</b></span>")
        self.result_label.set_markup(f"<span foreground='red'><b>{query.split('?')[0]}</b></span>")

        for child in self.result_grid.get_children():
            self.result_grid.remove(child)

        if not data:
            return
		#Despues de probar lo otro de ordenar y ver que no funcionaba he hecho esto:
        if "timetables" in query:
            now = datetime.now()
            weekDays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            today = now.strftime("%a")
            timeNow = now.strftime("%H:%M")

            def timetableOrdenado(entry):
                diaHoy = entry["day"]
                horaHoy = entry["hour"]
                difDias = (weekDays.index(diaHoy) - weekDays.index(today)) % 7
                clasePasada = difDias == 0 and horaHoy <= timeNow
                return (difDias + (7 if clasePasada else 0), horaHoy)

            data.sort(key=timetableOrdenado)

		#headers = list(data[0].keys())
        #Solo las que queremos
        headers = [h for h in data[0].keys() if h not in ("id", "student_id")]

		#Me he peleado a más no poder co esto, porque no había manera de que me saliera bien
        #ahora está como mejor me ha salido y creo que no lo voy a cambiar
        for i, header in enumerate(headers):
            label = Gtk.Label(label=header)
            label.set_name("result-header")
            label.get_style_context().add_class("header-cell")
            label.set_hexpand(True)
            label.set_halign(Gtk.Align.FILL)
            self.result_grid.attach(label, i, 0, 1, 1)

        for row_idx, row in enumerate(data):
            for col_idx, key in enumerate(headers):
                value = str(row[key])
                cell_label = Gtk.Label(label=value)
                cell_label.set_name("result-cell")

                clase = "even-cell" if row_idx % 2 == 0 else "odd-cell"
                cell_label.get_style_context().add_class(clase)

                cell_label.set_hexpand(True)
                cell_label.set_halign(Gtk.Align.FILL)
                self.result_grid.attach(cell_label, col_idx, row_idx + 1, 1, 1)

        self.show_all()

if __name__ == "__main__":
    win = CourseManager()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
