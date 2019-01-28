from bluez_components.characteristic import Characteristic


class LedChrc(Characteristic):
    BASE_LED_UUID = '12345678-1234-5678-1234-56789abcff67'

    def color_to_int(color_value):
        return {
            "red": '0',
            "yellow": '1',
            "green": '2'
        }.get(color_value, '0')

    def color_to_int(int_value):
        return {
            '0': "red",
            '1': "yellow",
            '2': "green"
        }.get(int_value, '0')
    
    def pin_from_color(color):
        return {
        "red": 16,
        "yellow": 20,
        "green": 21
    }.get(color, '0')

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            BASE_LED_UUID,  # use the row number to build the UUID
            ['read', 'write', 'write-without-response'],
            service)
        self.value = [0x00, 0x00]

    def ReadValue(self, options):
        print('RowCharacteristic Read: Row: ' + ' ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('RowCharacteristic Write: Row: ' + ' ' + repr(value))
        # toggle_led(int(value[0]), int(value[1]))
        self.value = value[:2]