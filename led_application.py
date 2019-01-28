from bluez_components.application import Application


class LedApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)

