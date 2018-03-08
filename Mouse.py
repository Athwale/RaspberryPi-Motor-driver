__author__ = 'Ondřej Mejzlík'
# V souboru /dev/input/mouse0 je hodnota v pohybu mysi v pixelech. Zaznamenavana data jsou po trojcich bytu.
# Prvni byte jsou tlacitka, druhy byte je pohyb po ose x (levo, pravo), treti byte je pohyb po y (dopredu, dozadu).
# Do souboru se zaznamenavaji znaky extended ASCII (255 hodnot).
# Funkce ord ziska decimalni hodnotu ascii znaku.
# Z DPI mysi lze vypocitat velikost jednoho pixelu senzoru mysi. DPI je pocet pixelu, ktery se vejde do delky jednoho
# palce (na primce nikoli ctverecnim palci). 1 palec je 25.4 mm. Mys predava data 1:1. Pohyb senzoru mysi o jeden pixel
# se rovna posunu kurzoru na obrazovce o jeden pixel. Vynasobenim velikosti pixelu v mm poctem ujetych pixelu, ziskame
# ujetou vzdalenost v mm.


class MouseReader:
    """
    Trida urcena pro cteni dat mysi.
    """
    __mouse = None
    # 1000 pro mys Microsof comfort mouse 4500
    # 1000 pro mys Microsoft wireless notebook mouse 4000
    # 1200 pro mys Genius Micro Traveler
    __mouse_dpi = 1200
    # Velikost pixelu senzoru mysi v mm
    __mouse_pixel_size = 25.4 / __mouse_dpi

    def __init__(self):
        """
        Konstruktor tridy cteni dat mysi. Otevre linuxovy soubor, kam mys zapisuje vystup.
        """
        self.__mouse = open("/dev/input/mouse0", "rb", 0)

    @staticmethod
    def __to_signed(number):
        """
        Metoda slouzi k prevodu vystupu mysi na cele cislo se znamenkem.
        :param number: Vstupni hodnota ze souboru mysi. Dekadicke cislo 0-255
        :return: Dekadicke cislo se znamenkem. O kolik pixelu se mys posunula.
        """
        return number - ((128 & number) << 1)

    def get_mouse_movement(self):
        """
        Metoda vraci o kolik mm se mys posunula jako dvojci x, y
        :return: Posun mysi, jako dvojce (x,y) v milimetrech.
        """
        # Mys uklada svuj vystup jako trojci bytu
        mouse_data = self.__mouse.read(3)

        # Rozebrani trojce bytu vystupu mysi na jednotlive casti
        buttons = mouse_data[0]
        pos_x = mouse_data[1]
        pos_y = mouse_data[2]

        # Vypocet ujete vzdalenosti v mm
        moved_x = self.__to_signed(pos_x) * self.__mouse_pixel_size
        moved_y = self.__to_signed(pos_y) * self.__mouse_pixel_size

        return moved_x, moved_y

'''
app = MouseReader()
total_x = 0
total_y = 0

try:
    while True:
        movement = app.get_mouse_movement()
        total_x += movement[0]
        total_y += movement[1]

except KeyboardInterrupt:
    print("Mouse moved by: " + str(total_x) + " mm on  X axis")
    print("Mouse moved by: " + str(total_y) + " mm on  Y axis")
'''