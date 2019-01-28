
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import sys

from random import randint
import RPi.GPIO as GPIO
from led_advertisement import LedAdvertisement
from led_application import LedApplication
from led_service import LedService
from led_characteristic import LedCharacteristic

from bluez_components.constants import *


def register_ad_cb():
    """
    Callback if registering advertisement was successful
    """
    print('Advertisement registered')


def register_ad_error_cb(error):
    """
    Callback if registering advertisement failed
    """
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


def register_app_cb():
    """
    Callback if registering GATT application was successful
    """
    print('GATT application registered')


def register_app_error_cb(error):
    """
    Callback if registering GATT application failed.
    """
    print('Failed to register application: ' + str(error))
    mainloop.quit()

def find_adapter_gattmanager(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if GATT_MANAGER_IFACE in props.keys():
            return o

    return None


def find_adapter_advertisingmanager(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props:
            return o
    return None


def get_service_manager(bus):
    # Get the GattManager
    adapter_gattmanager = find_adapter_gattmanager(bus)
    if not adapter_gattmanager:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter_gattmanager),
        GATT_MANAGER_IFACE)

    return service_manager


def get_ad_manager(bus):
    # Get the AdapterManager
    adapter_advertisingmanager = find_adapter_advertisingmanager(bus)
    if not adapter_advertisingmanager:
        print('LEAdvertisingManager1 interface not found')
        return

    adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter_advertisingmanager),
                                   "org.freedesktop.DBus.Properties")

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter_advertisingmanager),
                                LE_ADVERTISING_MANAGER_IFACE)

    return ad_manager

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(26, GPIO.IN)

def setup_application(bus):

    # Create gatt services
    application = LedApplication(bus)


def setup_service(bus):

    service = LedService(bus, 0)
    characteristic = LedCharacteristic(bus, 0, service)
    service.add_characteristic(service)
    return service

def setup_characteristic(bus):
    return LedCharacteristic()

def setup_advertisement(bus):
    
    # Create advertisement
    return LedAdvertisement(bus, 0)

mainloop = None

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus() 

    # Get ServiceManager and AdvertisingManager
    service_manager = get_service_manager(bus)
    ad_manager = get_ad_manager(bus)

    # GObject.threads_init()
    mainloop = GObject.MainLoop()

    application = setup_application(bus)
    service = setup_service(bus)
    application.add_service(service)

    # Register gatt services
    service_manager.RegisterApplication(application.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    test_advertisement = setup_advertisement(bus)

    # Register advertisement
    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)
    print(application)


    GObject.timeout_add(1000, readInput)

    print('running mainloop\n')

    inputThread = threading.Thread(name='input', target=readInput)
    try:
        mainloop.run()
        inputThread.start()
        print('started input')
    except KeyboardInterrupt:
        print("interupt")
        GPIO.cleanup()
        application_killed = True
        inputThread.stop()
        mainloop.quit()

if __name__ == '__main__':
    main()