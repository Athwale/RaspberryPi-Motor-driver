import threading

__author__ = 'Ondřej Mejzlík'

from tkinter import *
from Driver import Driver


class App:
    """
    Trida grafickeho rozhrani GUI
    """
    __text_area = None
    __syntax_label_text = None
    __next_command_text = None
    __syntax_label = None
    __driver = None
    __frame = None
    __driver_thread = None

    def __init__(self, tk):
        """
        Konstruktor pro GUI. Vyrobi hlavni frame, do ktereho vlozi textove pole a tlacitko.
        :param tk: tkinter okno
        """
        self.__frame = Frame(tk)
        # atributy fill a expand potreba kvuli zmene velikosti okna
        self.__frame.pack(fill=BOTH, expand=1)
        # sticky parametr u grid se pouziva aby prvek vedel, ke kterym stenam se musi prilepit
        # Pri pouzivani frame musime pouzivat grid, jinak se prvek nezobrazi
        # Sticky W prilepi label doleva
        Label(self.__frame, text="Use Ctrl+r to start").grid(row=0, column=0, sticky='W')
        Label(self.__frame, text="Use Ctrl+c to stop").grid(row=1, column=0, sticky='W')

        self.__syntax_label_text = StringVar()
        self.__syntax_label_text.set('')
        self.__syntax_label = Label(self.__frame, textvariable=self.__syntax_label_text)
        self.__syntax_label.grid(row=3, column=0, sticky='W')

        self.__next_command_text = StringVar()
        Label(self.__frame, textvariable=self.__next_command_text).grid(row=3, column=0, sticky='E', columnspan=3)

        scrollbar = Scrollbar(self.__frame)
        scrollbar.grid(row=2, column=1, sticky=W+E+N+S)
        # Textovy box pro zadavani prikazu
        self.__text_area = Text(self.__frame, height=15, width=25, bg="white", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.__text_area.yview)
        self.__text_area.grid(row=2, column=0)
        self.__text_area.insert(END, "/ Example program\nFW 1 cm")
        # Textovemu poli pridame hlidac udalosti klavesnice na kombinaci ctrl+r, cimz se spusti program.
        # Spoustet mysi pres tlacitko je neprakticke, protoze mys ujede pri pohybu robota.
        self.__text_area.bind("<Control-r>", func=self.__keyboard_handler_run)
        self.__text_area.bind("<Control-c>", func=self.__keyboard_handler_stop)
        # self.__text_area.insert(END, "/ Example program\nFW 10 cm\nR\nFW 10 cm\nR\nFW 10 cm\nR\nFW 10 cm\nR")

        self.__driver = Driver()

    def __run(self):
        if self.__parse():
            # Preklesleni okna po nastaveni novych textu
            self.__frame.update_idletasks()
            number_of_lines = int(self.__text_area.index("end").split(".", 1)[0])-1
            for row in range(number_of_lines):
                # range zacina od 0, ale indexy textu se pocitaji od 1
                row += 1
                first_index = str(row) + ".0"
                last_index = str(row) + ".end"
                line = self.__text_area.get(first_index, last_index)
                # Komentare preskakovat
                if line[0] == '/':
                    continue

                # Vyplneni nasledujiciho prikazu do textu
                self.__fill_next_command(row, number_of_lines)

                # Spusteni prikazu na aktualnim radku pomoci spusteni noveho vlakna
                self.__driver_thread = threading.Thread(target=self.__driver.drive, args=(line,))
                self.__driver_thread.start()
        else:
            # Vykreslime do GUI zmenene texty z metody parse
            self.__frame.update_idletasks()

    def __fill_next_command(self, row, number_of_lines):
        """
        Vyplni text dalsiho prikazu do label v gui na zaklade predaneho poctu radku v textovem poli a aktualniho radku.
        :param row: Aktualni radek
        :param number_of_lines: Pocet vsech radku v textovem poli
        """
        row += 1
        # Kdyz uz zadny dalsi prikaz neni, vypiseme END
        if row > number_of_lines:
            self.__next_command_text.set('Next: END')
            self.__frame.update_idletasks()
        else:
            first_index = str(row) + ".0"
            last_index = str(row) + ".end"
            next_command = self.__text_area.get(first_index, last_index)
            self.__next_command_text.set('Next: ' + next_command)
            self.__frame.update_idletasks()

    def __keyboard_handler_run(self, event):
        """
        Spousti zapsany program
        :param event: Neni pouzity
        """
        self.__run()

    def __keyboard_handler_stop(self, event):
        """
        Zastavi chod robota
        :param event: Neni pouzity
        """
        print('ctrl+c')
        if not self.__driver_thread is None:
            if self.__driver_thread.isAlive:
                self.__driver.stop()
                print("stop thread")

    def __parse(self):
        """
        Projde radek po radku a zkontroluje format zapsanych instrukci.
        Instrukce maji format: prikaz cislo:jednotka napriklad FW 10 cm nebo L otoceni doleva. Kazda instrukce je na
        vlastnim radku.
        Hlida omezeni na 10 000 radku.
        :rtype : True pokud je vse v poradku, False jinak.
        """
        # metoda index vraci retezec jako cislo.cislo - radek/slupec hledaneho znaku. End je konec, ale na konci je
        # pridan jeste znak noveho radku. Split rozdeli retezec podle separatoru a vraci seznam. Odecita se 1 kvuli
        # pridanemu novemu radku.
        number_of_lines = int(self.__text_area.index("end").split(".", 1)[0])-1
        if number_of_lines > 10000:
            self.__syntax_label.configure(fg='red')
            self.__syntax_label_text.set('Maximum 10 000 lines allowed')
            return False

        for row in range(number_of_lines):
            # range zacina od 0, ale indexy textu se pocitaji od 1
            row += 1
            first_index = str(row) + ".0"
            last_index = str(row) + ".end"
            # Format indexovani textu je: radek.sloupec, radek.sloupec
            line = self.__text_area.get(first_index, last_index)

            # Druhy parametr udava pocet rozdeleni, zbytek retezce bude v poslednim prvku seznamu
            try:
                split = line.split(" ", -1)
                if len(split) > 3:
                    self.__syntax_label.configure(fg='red')
                    self.__syntax_label_text.set('Wrong command format')
                    return False

                # Komentare ignorovat
                elif split[0][0] == '/':
                    continue

                elif split[0] == "FW" or split[0] == "BW" or split[0] == "fw" or split[0] == "bw":
                    if int(split[1]) > 0 and int(split[1]) <= 1000000:
                        if split[2] == 'mm' or split[2] == 'cm' or split[2] == 'm':
                            self.__syntax_label.configure(fg='blue')
                            self.__syntax_label_text.set('Syntax OK')
                        else:
                            self.__syntax_label.configure(fg='red')
                            self.__syntax_label_text.set('Only mm/cm/m allowed')
                            return False
                    else:
                        if int(split[1]) < 0:
                            self.__syntax_label.configure(fg='red')
                            self.__syntax_label_text.set('Negative numbers not allowed')
                            return False
                        elif int(split[1]) > 1000000:
                            self.__syntax_label.configure(fg='red')
                            self.__syntax_label_text.set('Values > 1000 000 not allowed')
                            return False

                elif split[0] == 'L' or split[0] == 'R' or split[0] == 'l' or split[0] == 'r':
                    if len(split) == 1:
                        self.__syntax_label.configure(fg='blue')
                        self.__syntax_label_text.set('Syntax OK')
                    else:
                        self.__syntax_label.configure(fg='red')
                        self.__syntax_label_text.set('L/R can not have parameters')
                        return False

                else:
                    self.__syntax_label.configure(fg='red')
                    if split[0] == '':
                        self.__syntax_label_text.set('Blank line not allowed')
                        return False
                    else:
                        self.__syntax_label_text.set('Only commands FW/BW/L/R allowed')
                        return False
            except ValueError:
                self.__syntax_label.configure(fg='red')
                self.__syntax_label_text.set('Number format error')
                return False
            except IndexError:
                self.__syntax_label.configure(fg='red')
                self.__syntax_label_text.set('Incomplete command found')
                return False

        return True

    def quit_it(self):
        self.__driver.end()
        root.quit()

root = Tk()
root.wm_title('App')
root.resizable(width=False, height=False)
# parametry geometry udavaji sirku, vysku, pozici x a y na monitoru
root.geometry("195x269+800+300")
gui = App(root)
# root.wm_protocol("WM_DELETE_WINDOW", gui.quit_it)
root.mainloop()
