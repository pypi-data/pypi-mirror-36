# relays_manager

Python wrapper for the ICStation relays.
It has been tested with the 4-Channel version but should work with the 1,2 and 8 channels.

# Installation
relays_manager is available on [pip](https://pypi.python.org/pypi/relays_manager). You can install it using :

``` shell
pip install relays-manager
```

# Documentation

## Functions
``
``
``

## Example code

``` python
from usb_manager import UsbManager
from relays_manager import RelayManager

# Show all usb devices with a vendor id of 1659
UsbManager().filterBy(vid="1659").show()

# Print the serial number of every devices with vendor id of 1659 and pid of 8963
print(UsbManager().filterBy(vid="1659", pid="8963").get("device"))
```

## Donation

This project helped you ? You can buy me a cup of coffee  
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=EWHGT3M9899J6)

