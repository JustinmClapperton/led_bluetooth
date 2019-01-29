from bluez_components.characteristic import Characteristic
import RPi.GPIO as GPIO
import pdb
from pins import *

class LedCharacteristic(Characteristic):
    BASE_LED_UUID = '12345678-1234-5678-1234-56789abcff67'

    def int_to_color(int_value):
        return {
            0: "red",
            1: "yellow",
            2: "green"
        }.get(int_value, '0')
    
    def pin_from_color(color):
        return {
        "red": RED_LED_PIN,
        "yellow": YELLOW_LED_PIN,
        "green": GREEN_LED_PIN
    }.get(color, '0')

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            LedCharacteristic.BASE_LED_UUID,  # use the row number to build the UUID
            ['read', 'write', 'write-without-response'],
            service)
        self.value = [0x00, 0x00]

    def ReadValue(self, options):
        print('RowCharacteristic Read: Row: ' + ' ' + repr(self.value))
        return self.value

    def WriteValue(self, value, options):
        print('RowCharacteristic Write: Row: ' + ' ' + repr(value))
        LedCharacteristic.toggle_led(int(value[0]), int(value[1]))
        self.value = value[:2]
    
    def toggle_led(color_index, on):
        color = LedCharacteristic.int_to_color(color_index)
        pin = LedCharacteristic.pin_from_color(color)
        if on: 
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)