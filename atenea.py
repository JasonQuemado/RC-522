import gi
import rfid_rc522
#import cssGraphic
import threading
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class Graphic(Gtk.Window):
    def __init__(self):
        super().__init__(title="ATENEA")
        self.set_default_size(600, 400)
        self.set_border_width(10)
        self.rfid = rfid_rc522.Rfid()

        #Cargamos el archivo CSS, la funcion esta abajo
        self.load_css()

        #Caja principal, aqui es donde anadimos todo
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        #Boton de estado del lector RFID el cual se actualiza si la tarjeat se ha leido
        self.botonAct = Gtk.Button()
        self.botonActShow = Gtk.Label()
        self.botonActShow.set_markup("<span>Please, log in with your university card</span>")
        self.botonAct.add(self.botonActShow)
        self.botonAct.set_name("main-button")
        self.botonAct.set_size_request(400, 250)

        #Label para mostrar el UID
        self.botonUid = Gtk.Label()
        self.botonUid.set_markup("<span>Waiting for card...</span>")
        self.botonUid.set_name("label-uid")

        #Boton para resetear el programa
        labelClear = Gtk.Label()
        labelClear.set_markup("<span>CLEAR</span>")
        self.botonClear = Gtk.Button()
        self.botonClear.add(labelClear)
        self.botonClear.set_name("clear-button")
        self.botonClear.set_size_request(400, 100)
        self.botonClear.connect("clicked", self.clear_display)

        #Aqui empaquetamos todos los botnes en la caja que creamos al principio
        box.pack_start(self.botonAct, True, True, 0)
        box.pack_start(self.botonUid, True, True, 0)
        box.pack_start(self.botonClear, True, True, 0)

        #Creamos un hilo separado para poder detectar las tarjetas
        self.rfid_thread = threading.Thread(target=self.lectorTarjeta)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()

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

    def lectorTarjeta(self):
        #Invocamos la clase que creamos en el puzzle 1
        try:
            uid = self.rfid.read_uid()
            if uid:
                GLib.idle_add(self.mostrar_uid, uid)
            else:
                GLib.idle_add(self.mostrar_error)
        except Exception as e:
            print(f"Error: {e}")
            GLib.idle_add(self.mostrar_error)

    #Aqui declaramos las funciones de los botones con las caracteristicas del archivo css que hemos creado
    def mostrar_uid(self, uid):
        self.botonAct.set_name("green-button")
        self.botonUid.set_markup(f"<span>Tarjeta detectada: {uid}</span>")
        self.botonActShow.set_markup("<span>Card detected succesfully!</span>")

    def mostrar_error(self):
        self.botonAct.set_name("red-button")
        self.botonUid.set_markup("<span>Error reading card!</span>")
        
    #Aqui en el clear indicamos lo que pasará después de pulsarlo y comenzamos el hilo de nuevo
    #Utilizamos daemon ya que son tareas/hilos que se pueden ejecutar en segundo plano
    def clear_display(self, widget):
        self.botonAct.set_name("main-button")
        self.botonUid.set_markup("<span>Waiting for card...</span>")
        self.botonActShow.set_markup("<span>Please, log in with your university card</span>")
        self.rfid_thread = threading.Thread(target=self.lectorTarjeta)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()


if __name__ == "__main__":
    atenea = Graphic()
    atenea.show_all()
    Gtk.main()
