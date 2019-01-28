import RPi.GPIO as GPIO
from led_advertisement import LedAdvertisement
from led_application import LedApplication
from led_service import LedService


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

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(13, GPIO.IN)
    GPIO.setup(26, GPIO.IN)

mainloop = None

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus() 

    # Get ServiceManager and AdvertisingManager
    service_manager = get_service_manager(bus)
    ad_manager = get_ad_manager(bus)

    # Create gatt services
    application = LedApplication(bus)

    # Create advertisement
    test_advertisement = LedAdvertisement(bus, 0)

    # GObject.threads_init()
    mainloop = GObject.MainLoop()

    # Register gatt services
    service_manager.RegisterApplication(application.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    print(application)

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