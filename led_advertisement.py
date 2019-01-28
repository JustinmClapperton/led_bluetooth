from bluez_components.advertisement import Advertisement


class LedAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.include_tx_power = True