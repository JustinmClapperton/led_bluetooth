from bluez_components.characteristic import Characteristic


class LedChrc(Characteristic):


    def color_to_int(color_value):
        return {
            "red": '0',
            "yellow": '1',
            "green": '2'
        }.get(color_value, '0')

    def get_led_uuid(color):
        return BASE_LED_UUID + color_to_int(color)

    def __init__(self, bus, index, service, color):
        Characteristic.__init__(
            self, bus, index,
            get_led_uuid(color),  # use the row number to build the UUID
            ['read', 'write', 'write-without-response'],
            service)
        self.value = [0x00, 0x00]
        self.color = color

    def ReadValue(self, options):
        print('RowCharacteristic Read: Row: ' + str(self.color) + ' ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('RowCharacteristic Write: Row: ' + str(self.color) + ' ' + repr(value))
        toggle_led(int(value[0]), int(value[1]))
        self.value = value[:2]