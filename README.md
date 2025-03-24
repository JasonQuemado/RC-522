This is how I got the code for the RFID_RC522 tag reader, and the solutions to the problems I encountered, as well as websites that helped me.

When isntalling the rc-522 libraries you have to install:
```
pip install mfrc522
```
instead of:
```
pip install pi-rc522
```

The pin configuration between the Rfid and the Raspberry is the following:

| RC-522 pins | Raspberry Pi pins |
| --- | --- |
| SDA | GPIO 24 |
| SCK | GPIO 23 |
| MOSI | GPIO 19 |
| MISO | GPIO 21 |
| IRQ |  |
| GND | GPIO 6 |
| RST | GPIO 22 |
| 3.3V | GPIO 1 |

At first I was using the MFRC522() import, which is more complex and has more functions, but it was giving me trouble with the *"request"* so I used the SimpleMFRC522() import, also explanied and specified on the first link.

Resources I used for guide:

Links
| ------------------ |
| https://pypi.org/project/mfrc522-python/ |
| https://docs.python.org/3/library/time.html |
| https://github.com/ondryaso/pi-rc522?tab=readme-ov-file |

In the future I will modify the code so that it can read multiple cards, and output the tag id of the card during an x period of time --> implemented!!


Código primera parte del Puzzle 2 sin CSS
-
```py
import gi
import rfid_rc522
import threading
#import cssGraphic

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


class Graphic(Gtk.Window):
    def __init__(self):
        super().__init__(title="ATENEA")
        self.set_default_size(600, 400)
        self.set_border_width(10)
        self.rfid = rfid_rc522.Rfid()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        self.botonAct = Gtk.Button()
        self.botonActShow = Gtk.Label()
        self.botonActShow.set_markup("<span font='30' weight='bold'>Please, log in with your university card</span>")
        self.botonAct.add(self.botonActShow)
        self.botonAct.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("blue"))
        self.botonAct.set_size_request(400, 250)

        self.botonUid = Gtk.Label()
        self.botonUid.set_markup("<span font='20' weight='bold'>Waiting for card...</span>")

        labelClear = Gtk.Label()
        labelClear.set_markup("<span font='20' weight='bold'>CLEAR</span>")
        self.botonClear = Gtk.Button()
        self.botonClear.add(labelClear)
        self.botonClear.set_size_request(400, 100)
        self.botonClear.connect("clicked", self.clear_display)

        box.pack_start(self.botonAct, True, True, 0)
        box.pack_start(self.botonUid, True, True, 0)
        box.pack_start(self.botonClear, True, True, 0)

        self.rfid_thread = threading.Thread(target=self.lectorTarjeta)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()

    def lectorTarjeta(self):
        lectorUid = self.rfid.read_uid()
        GLib.idle_add(self.mostrar_uid, lectorUid)

    def mostrar_uid(self, lectorUid):
        self.botonAct.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("green"))
        self.botonUid.set_markup(f"<span font='20' weight='bold' color='green'>Card ID: {lectorUid}</span>")
        self.botonActShow.set_markup(f"<span font='30' weight='bold'>Card detected succesfully!</span>")

    def clear_display(self, widget):
        self.botonAct.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("blue"))
        self.botonUid.set_markup("<span font='20' weight='bold'>Waiting for card...</span>")
        self.botonActShow.set_markup("<span font='30' weight='bold'>Please, log in with your university card</span>")
        self.rfid_thread = threading.Thread(target=self.lectorTarjeta)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()


if __name__ == "__main__":
    atenea = Graphic()
    atenea.show_all()
    Gtk.main()


```
