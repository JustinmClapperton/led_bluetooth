from bluez_components.characteristic import Characteristic
from bluez_components.constants import *
import dbus
import pdb

class IphoneLedCharacteristic(Characteristic):
    """
    Fake Battery Level characteristic. The battery level is drained by 2 points
    every 5 seconds.

    """
    IPHONE_LED_UUID = '12345678-1234-5678-1234-56789abcff68'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.IPHONE_LED_UUID,
                ['read', 'notify'],
                service)
        self.notifying = False
        self.value = {"color_int": 0, "on": 0}

    def notify_led_changed(self, color_int, on):
        if not self.notifying:
            return
        self.value = {"color_int": color_int, "on": on}
        self.PropertiesChanged(
                GATT_CHRC_IFACE,
                { 'Value': [dbus.Byte(self.value["color_int"]), dbus.Byte(self.value["on"])] }, [])

    def ReadValue(self, options):
        print('Battery Level read: ' + repr(self.value))
        return [dbus.Byte(self.value["color_int"]), dbus.Byte(self.value["on"])]

    def StartNotify(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        self.notifying = True


    def StopNotify(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        self.notifying = False