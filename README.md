Links used for guide:
| https://pypi.org/project/mfrc522-python/ | |
| https://docs.python.org/3/library/time.html | |
| https://github.com/ondryaso/pi-rc522?tab=readme-ov-file | |

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

In the future I will modify the code so that it can read multiple cards, and output the tag id of the card during an x period of time
