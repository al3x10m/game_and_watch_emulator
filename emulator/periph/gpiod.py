from .periph import Periph

"""
D0  = BUTTON_UP
D5  = BUTTON_B
D9  = BUTTON_A
D11 = BUTTON_LEFT
D14 = BUTTON_DOWN
D15 = BUTTON_RIGHT
"""

class GPIOD(Periph):
    BASE_ADDR = 0x5802_0C00

    def __init__(self):
        self._MODER = 0xFFFF_FFFF
        self._OTYPER = 0
        self._OSPEEDR = 0
        self._PUPDR = 0
        self._IDR = 1 << 15 | 1 << 14 | 1 << 11 | 1 << 9 | 1 << 5 | 1
        self._ODR = 0
        self._BSRR = 0
        self._LCKR = 0
        self._AFRL = 0
        self._AFRH = 0

    def read_mem(self, address: int, size: int) -> int:
        if address == self.BASE_ADDR:
            return self._MODER
        elif address == self.BASE_ADDR + 0x4:
            return self._OTYPER
        elif address == self.BASE_ADDR + 0x8:
            return self._OSPEEDR
        elif address == self.BASE_ADDR + 0xC:
            return self._PUPDR
        elif address == self.BASE_ADDR + 0x10:
            return self._IDR
        elif address == self.BASE_ADDR + 0x14:
            return self._ODR
        elif address == self.BASE_ADDR + 0x1C:
            return self._LCKR
        elif address == self.BASE_ADDR + 0x20:
            return self._AFRL
        elif address == self.BASE_ADDR + 0x24:
            return self._AFRH
        return 0

    def write_mem(self, address: int, size: int, data: int):
        if address == self.BASE_ADDR:
            self.set_reg('_MODER', 0xFFFF_FFFF, data)
        elif address == self.BASE_ADDR + 0x4:
            self.set_reg('_OTYPER', 0x0000_FFFF, data)
        elif address == self.BASE_ADDR + 0x8:
            self.set_reg('_OSPEEDR', 0xFFFF_FFFF, data)
        elif address == self.BASE_ADDR + 0xC:
            self.set_reg('_PUPDR', 0xFFFF_FFFF, data)
        elif address == self.BASE_ADDR + 0x14:
            self.set_reg('_ODR', 0x0000_FFFF, data)
        elif address == self.BASE_ADDR + 0x18:
            self.set_reg('_BSRR', 0xFFFF_FFFF, data)
        elif address == self.BASE_ADDR + 0x1C:
            self.set_reg('_LCKR', 0x0001_FFFF, data)
        elif address == self.BASE_ADDR + 0x20:
            self.set_reg('_AFRL', 0xFFFF_FFFF, data)
        elif address == self.BASE_ADDR + 0x24:
            self.set_reg('_AFRH', 0xFFFF_FFFF, data)
