from rfid_rc522 import*
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, Gdk

class Atenea(Gtk.Window):
    def __init__(self):
        super().__init__(title="ATENEA")
        self.set_default_size(600, 400)
        self.set_border_width(10)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box) #Permite tener mas de un boton

        self.botonAct = Gtk.Button(label="Please, log in with your university card")
        self.botonAct.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("blue"))
        #self.botonAct.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("blue"))
        self.botonAct.set_size_request(400,250)
        self.botonAct.connect("clicked", self.cambiar_color)
        
        #Esto no ha funcionado porque habia que crear un label primero
        #self.botonClear = Gtk.Button()
        #self.botonClear.set_label("<span font='30' weight='bold'>CLEAR</span>")
        #self.botonClear.set_use_markup(True)  # Activa HTML en el label
        #self.botonAct.set_size_request(400,150)
        
        labelClear = Gtk.Label()
        labelClear.set_markup("<span font='30' weight='bold'>CLEAR</span>")
        
        self.botonClear = Gtk.Button()
        self.botonClear.add(labelClear)
        self.botonClear.set_size_request(400, 100)
        
        box.pack_start(self.botonAct, True, True, 0)
        box.pack_start(self.botonClear, True, True, 0)
		
    def cambiar_color(self, widget):
        widget.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))  # Cambia color


atenea = Atenea()
atenea.show_all()
Gtk.main()
