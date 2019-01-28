from bluez_components.service import Service


class LedService(Service):

    LED_SVC_UUID = '12345678-1234-5678-1234-56789abc0010'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, LedService.LED_SVC_UUID, True)