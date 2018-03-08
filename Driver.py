__author__ = 'Ondřej Mejzlík'

from Mouse import MouseReader
from Controller import MotorController
import time


class Driver:
    """
    Trida urcena pro ovladani motoru na zaklade prikazu predanych z GUI.
    K ovladani smeru otaceni motoru vyuziva tridu Controller, ktera umi vyrizovat zakladni povely.
    """
    __motor_controller = None

    def __init__(self):
        """
        Konstruktor tridy Driver. Vyrobi instanci motor controller pro dalsi pouziti v metodach.
        """
        self.__motor_controller = MotorController()

    def end(self):
        """
        Metoda slouzi k zastaveni chodu motoru a nastaveni GPIO do vychozich hodnot.
        """
        self.__motor_controller.stop()
        self.__motor_controller.clean()

    def stop(self):
        """
        Metoda slouzi k zastaveni chodu motoru.
        """
        self.__motor_controller.stop()

    def __forward(self, distance):
        """
        Metoda popojede robotem dopredu o stanoveny pocet milimetru.
        :param distance: Kolik mm se ma ujet smerem dopredu
        """
        self.__motor_controller.forward()
        # Kolik mm jsme jiz ujeli
        moved_by = 0
        # Mouse reader nelze vytvorit v konstruktoru, protoze to zpusobuje problemy s duplikaci dat zrejme kvuli bufferu
        mouse_reader = MouseReader()
        while moved_by < distance:
            # Get_mouse_movement vraci dvojci (x,y). Pohyb dopredu je osa y.
            mouse_data = mouse_reader.get_mouse_movement()
            moved_by += mouse_data[1]

        # Motory maji setrvacnost, aby se stanovena vzdalenost ujela co nejpresneji, ne potreba na konci na zlomek
        # sekundy obratit polaritu motoru a zrusit tak ucinek setrvacnosti
        self.__motor_controller.stop()
        self.__motor_controller.backward()
        time.sleep(0.065)
        self.__motor_controller.stop()

    def __backward(self, distance):
        """
        Metoda popojede robotem dozadr o stanoveny pocet milimetru.
        :param distance: Kolik mm se ma ujet smerem dozadu
        """
        self.__motor_controller.backward()
        mouse_reader = MouseReader()
        while distance > 0:
            mouse_data = mouse_reader.get_mouse_movement()
            # Pricitame zapornou hodnotu
            distance += mouse_data[1]
        self.__motor_controller.stop()

    def __left(self):
        """
        Metoda otoci robota o 90 stupnu doleva
        """
        print("doleva")

    def __right(self):
        """
        Metoda otoci robota o 90 stupnu doprava
        """
        print("doprava")

    def drive(self, instruction):
        """
        Metoda rozebere instrukci a podle ni spusti prislusnou akci pohybu robota
        :param instruction: instrukce predana z GUI
        """
        # Jakmile se zavola znovu metoda drive, predchozi prikaz se musi zastavit.
        self.__motor_controller.stop()

        instruction = instruction.lower()
        parts = instruction.split(" ", -1)
        # Pokud je delka 1, jde o zataceni.
        if len(parts) == 1:
            # Zatacime doleva
            if parts[0] == 'l':
                self.__left()

            # Zatacime doprava
            elif parts[0] == 'r':
                self.__right()

        # Pokud je delka 3, jedeme dopredu nebo dozadu
        elif len(parts) == 3:
            # Zadanou vzdalenost k ujeti chceme vzdy v mm
            distance = 0
            if parts[2] == 'mm':
                distance = int(parts[1])
            elif parts[2] == 'cm':
                distance = int(parts[1]) * 10
            elif parts[2] == 'm':
                distance = int(parts[1]) * 1000

            # Jedeme dopredu
            if parts[0] == 'fw':
                self.__forward(distance)

            # Jedeme dozadu
            elif parts[0] == 'bw':
                self.__backward(distance)