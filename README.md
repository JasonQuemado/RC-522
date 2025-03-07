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
