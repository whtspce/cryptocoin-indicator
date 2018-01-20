# Author: Samuel D. Relton
# Email: samuel.relton@manchester.ac.uk
# Website: www.samrelton.com
# BTC Tips: 1N1cN6V4AwcibwzSXC2fywB6NorSwRAEpd

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GObject as gobject
import signal
import os
import requests

APPINDICATOR_ID = "cryptocoin-indicator"

# Notes: Change icon dynamically with indicator.set_icon()

# Global variable for function to collect updated prices
# Default to BTCUSD on BitFinex
global currentupdate

# Quit indicator
def quit(source):
    gtk.main_quit()


##############################
# Update Prices
##############################
def update_btcusd_yobit():
    url = r"https://yobit.net/api/3/ticker/btc_usd"
    response = requests.get(url)
    data = response.json()
    price = data["btc_usd"]["last"]
    price = str(round(float(price), 3))
    mystring = "BTCUSD: " + price
    return mystring


def set_update_btcusd_yobit(source):
    global currentupdate
    currentupdate = update_btcusd_yobit

# ##############################
# # Initialization
# ##############################


# # Default to BTCUSD from Yobit
currentupdate = update_btcusd_yobit


# Update prices
def update_price(indicator):
    curprice = currentupdate()
    indicator.set_label(curprice, "BTCUSDX: 1000.32112")
    return True


##############################
# Create menu
##############################
def build_menu():
    menu = gtk.Menu()

    # Which price to display
    btcusd_yobit = gtk.MenuItem("BTCUSD: Yobit")
    btcusd_yobit.connect("activate", set_update_btcusd_yobit)
    menu.append(btcusd_yobit)

    # Separator
    menu.append(gtk.SeparatorMenuItem())

    # Quit
    item_quit = gtk.MenuItem("Quit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


##############################
# Main function
##############################
def main():
    # Set up indicator

    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        # os.path.abspath('cryptocoin-indicator.svg'),
        os.path.abspath('bitcoin-512.png'),
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    indicator.set_label("BTCUSD: ...", "BTCUSD: 1000.32")

    # Allow stop signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Update prices every 2 seconds
    updatetimer = gobject.timeout_add(20000, update_price, indicator)

    # Start main loop
    gtk.main()


if __name__ == "__main__":
    main()
