__author__ = 'Ondřej Mejzlík'

# Vyzkousime importovat modul GPIO, coz lze pouze jako root
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Can not import RPi.GPIO. Run script as root.")


class MotorController:
    """
    Trida urcena pro rizeni motoru. Umi zapnout chod dopredu, dozadu, doleva, doprava, zastavit a vynulovat GPIO piny.
    Umi vypsat informace o pouzitych pinech.
    """
    # Nastaveni vystupnich pinu pro ovladani motoru
    __left_backward = 5
    __left_forward = 6
    __right_backward = 13
    __right_forward = 19

    def __init__(self):
        """
        Konstruktor tridy ovladace motoru. Nastavi cislovani GPIO pinu podle oznanceni portu
        a nastavi zvolene piny jako vystupni.
        """
        # Pred inicializaci, smazeme predchozi nastaveni.
        # Pokus vymazat nastaveni nenastavenych pinu vyhodi varovani, to ocekavame a nechceme vypisovat.
        GPIO.setwarnings(0)
        GPIO.cleanup()
        # Nastaveni GPIO na cislovani podle oznaceni portu, nikoli podle cislovani konektoru
        GPIO.setmode(GPIO.BCM)
        # Definovani pinu jako vystupnich
        GPIO.setup(self.__left_forward, GPIO.OUT)
        GPIO.setup(self.__left_backward, GPIO.OUT)
        GPIO.setup(self.__right_forward, GPIO.OUT)
        GPIO.setup(self.__right_backward, GPIO.OUT)

    def forward(self):
        """
        Metoda pro pohyb dopredu. Oba dva motory spusti smerem dopredu
        Pred spustenim motoru je nutne predchozi nastaveni GPIO pinu vynulovat
        """
        GPIO.output(self.__left_forward, GPIO.HIGH)
        GPIO.output(self.__right_forward, GPIO.HIGH)
        print("Going forward")

    def backward(self):
        """
        Metoda pro pohyb dozadu. Oba dva motory spusti smerem dozadu
        """
        GPIO.output(self.__left_backward, GPIO.HIGH)
        GPIO.output(self.__right_backward, GPIO.HIGH)
        print("Going backward")

    def left(self):
        """
        Metoda pro otoceni doleva. Levy motor spusti pozpatku a pravy dopredu
        """
        GPIO.output(self.__left_backward, GPIO.HIGH)
        GPIO.output(self.__right_forward, GPIO.HIGH)
        print("Turning left")

    def right(self):
        """
        Metoda pro otoceni doprava. Levy motor spusti dopredu a pravy pozpatku
        """
        GPIO.output(self.__left_forward, GPIO.HIGH)
        GPIO.output(self.__right_backward, GPIO.HIGH)
        print("Turning right")

    def stop(self):
        """
        Metoda pro zastaveni. Vypne vsechny GPIO piny ovladajici smer motoru
        """
        GPIO.output(self.__left_forward, GPIO.LOW)
        GPIO.output(self.__left_backward, GPIO.LOW)
        GPIO.output(self.__right_forward, GPIO.LOW)
        GPIO.output(self.__right_backward, GPIO.LOW)
        print("Stop motors")

    @staticmethod
    def clean():
        """
        Metoda pro vynulovani nastaveni GPIO pri konci programu
        """
        GPIO.cleanup()
        print("Stop cleanup")

    def info(self):
        """
        Vypisuje informace o pouzitych pinech
        """
        print("Using GPIO pins:")
        print("Left forward " + str(self.__left_forward))
        print("Left backward " + str(self.__left_backward))
        print("Right forward " + str(self.__right_forward))
        print("Right backward " + str(self.__right_backward))