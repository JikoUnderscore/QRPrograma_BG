import cv2
import kivy
import pyzbar
from pyzbar import pyzbar
from os import listdir
from os import path
import csv
import itertools
from datetime import datetime
import win32ctypes.core
import pkg_resources

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

# INSTALL - https://www.youtube.com/watch?v=mUdnjNGePZw&ab_channel=MachineLearningHub


class Grid_to(GridLayout):
    def __init__(self, **kwargs):
        super(Grid_to, self).__init__(**kwargs)
        self.cols = 2
        self.fontt = 23

        self.fajil = Label(text=f"ИЗБРАНА ТАБЛИЦА:\n{self.last_table_get()}", font_size=self.fontt)
        self.add_widget(self.fajil)
        self.spinner = Spinner(text='избери', font_size=self.fontt)
        self.spinner.bind(text=self.get_name_of_table)
        self.spinner.bind(on_press=self.file_sercher)
        self.add_widget(self.spinner)

        self.add_widget(Label(text="ДАТА*   [ref=world][color=FF0000][i]/ГГГГ–ММ–ДД/[/i][/color][/ref]", font_size=self.fontt, markup=True))
        self.data_vyv = TextInput(multiline=False, font_size=self.fontt, write_tab=False)
        self.data_vyv.bind(focus=self.make_it_white)
        self.add_widget(self.data_vyv)

        self.add_widget(Label(text="ПРИХОДИ*", font_size=self.fontt))
        self.prihodi_vyv = TextInput(multiline=False, text='0', font_size=self.fontt, write_tab=False, input_filter='float')
        self.prihodi_vyv.bind(focus=self.make_it_white)
        self.add_widget(self.prihodi_vyv)

        self.add_widget(Label(text="РАЗХОДИ*", font_size=self.fontt))
        self.razhodi_vyv = TextInput(multiline=False, text='0', font_size=self.fontt, write_tab=False, input_filter='float')
        self.razhodi_vyv.bind(focus=self.make_it_white)
        self.add_widget(self.razhodi_vyv)

        self.add_widget(Label(text="описание", font_size=self.fontt))
        self.opisanie_vyv = TextInput(multiline=True, font_size=self.fontt, write_tab=False)
        self.add_widget(self.opisanie_vyv)

        self.add_widget(Label(text="№ на фискална памет", font_size=self.fontt))
        self.dr1_vyv = TextInput(multiline=False, font_size=self.fontt, write_tab=False)
        self.add_widget(self.dr1_vyv)

        self.add_widget(Label(text="№ на касова бележка", font_size=self.fontt))
        self.dr2_vyv = TextInput(multiline=False, font_size=self.fontt, write_tab=False)
        self.add_widget(self.dr2_vyv)

        self.run_camera = Button(text="Включи камерата", font_size=self.fontt)
        self.run_camera.bind(on_press=lambda e: [print(e), self.turn_on_camera()])
        self.add_widget(self.run_camera)

        self.rycno = Button(text="Запази", font_size=self.fontt)
        self.rycno.bind(on_press=self.submitt)
        self.add_widget(self.rycno)

    def make_it_white(self,e_widget, istrue):
        if istrue:
            e_widget.background_color = (1, 1, 1, 1)


    def get_name_of_table(self, e, selected_text=None):
        print(e)
        self.fajil.text = f'ИЗБРАНА ТАБЛИЦА:\n{selected_text}'
        self.last_table_set(selected_text)

    def file_sercher(self, e):
        print(e, 'here')
        filess = []
        for nameoffile in listdir('.'):
            if nameoffile.endswith('.csv'):
                filess.append(nameoffile.replace('.csv', ''))

        self.spinner.values = filess

    def last_table_set(self, pos=None):
        if pos == None:
            pos = 'няма'
        with open("posledna_tablica.dat", mode='w', encoding='utf-8') as file:
            file.write(pos)

    def last_table_get(self):
        try:
            with open("posledna_tablica.dat", mode='r', encoding='utf-8') as file2:
                vfaila = file2.read()
                return vfaila
        except Exception:
            self.last_table_set()
            return 'нема'

    def table_maker(self, data, prihodi=float, razhodi=float, opisanie=None, fiskalna_pamet=None, kasova_belezka=None):
        # with open("bposleden_barkod.dat", mode='r') as file:
        #     fajl = file.read().split('*')
        ime_na_tablica = self.fajil.text.split('\n')[1]


        pole = ['дата', 'приходи', 'разходи', 'описание', '№ на фискална памет', '№ на касова бележка',
                'ПРИХОДИ/РАЗХОДИ']
        d = {'дата': data, 'приходи': prihodi, 'разходи': razhodi, 'описание': opisanie,
             '№ на фискална памет': fiskalna_pamet, '№ на касова бележка': kasova_belezka, 'ПРИХОДИ/РАЗХОДИ': None}

        if path.exists(f"{ime_na_tablica}.csv"):
            with open(f"{ime_na_tablica}.csv", "a", newline='', encoding="utf-8-sig") as tablica:
                csv_pisac = csv.DictWriter(tablica, fieldnames=pole)
                csv_pisac.writerow(d)
                # print(d)

        else:
            with open(f"{ime_na_tablica}.csv", "w", newline='', encoding="utf-8-sig") as tablica:
                csv_pisac = csv.DictWriter(tablica, fieldnames=pole)
                csv_pisac.writeheader()
                csv_pisac.writerow({'дата': None, 'приходи': 0, 'разходи': 0, 'описание': None,
                                    '№ на фискална памет': None, '№ на касова бележка': None, 'ПРИХОДИ/РАЗХОДИ': None})
                csv_pisac.writerow(d)

        # sorting and removing duplicated
        with open(f"{ime_na_tablica}.csv", "r", newline='', encoding="utf-8-sig") as csv_data_reader:
            reader = csv.reader(csv_data_reader)
            next(csv_data_reader)
            twoDlist = list(reader)
            # print(nnn)

            twoDlist.sort()
            days_sorted = list(num for num, _ in itertools.groupby(twoDlist))
            # print(days_sorted)

            obst_prihodi = 0.00
            obst_razhodi = 0.00

            for line in days_sorted:
                obst_prihodi += float(line[1])
                obst_razhodi += float(line[2])

            for i, line in enumerate(days_sorted):
                if i == 0:
                    line.insert(6, f"{obst_prihodi:.2f}/{obst_razhodi:.2f} = {obst_prihodi - obst_razhodi:.2f}")
                else:
                    line.insert(6, None)

            # days_sorted = sorted(twoDlist, key=lambda day: datetime.strptime(day[0], "%Y-%m-%d"), reverse=False)
            # print(days_sorted)

        # writing the sorted
        with open(f"{ime_na_tablica}.csv", "w", newline='', encoding="utf-8-sig") as tablica:
            csv_pisac = csv.DictWriter(tablica, fieldnames=pole)
            csv_pisac.writeheader()

            for line in days_sorted:
                dictionary = dict(zip(pole, line))
                csv_pisac.writerow(dictionary)

    def submitt(self, e):
        print(e)
        self.data_vyv.background_color = (1, 1, 1, 1)
        self.prihodi_vyv.background_color = (1, 1, 1, 1)
        self.razhodi_vyv.background_color = (1, 1, 1, 1)
        if self.data_vyv.text == '' or self.prihodi_vyv.text == '' or self.razhodi_vyv.text == '':
            ivalid = Ppo()
            greska_tekst = ''
            if self.data_vyv.text == '':
                self.data_vyv.background_color = (1, 0, 0, 0.8)
                greska_tekst += 'Попълнете полето за ДАТА \n'
            if self.prihodi_vyv.text == '':
                self.prihodi_vyv.background_color = (1, 0, 0, 0.8)
                greska_tekst += 'Попълнете полето за ПРИХОДИ \n'
            if self.razhodi_vyv.text == '':
                self.razhodi_vyv.background_color = (1, 0, 0, 0.8)
                greska_tekst += 'Попълнете полето за РАЗХОДИ \n'

            ivalid.add_widget(Label(text=greska_tekst))
            print(len(greska_tekst))
            ivalid.show_pop()

        elif self.data_vyv.text != '' or self.prihodi_vyv.text != '' or self.razhodi_vyv.text != '':
            vjarna_data = False
            try:
                datetime.strptime(self.data_vyv.text, '%Y-%m-%d')
                vjarna_data = True

                float(self.prihodi_vyv.text)
                float(self.razhodi_vyv.text)

                self.table_maker(self.data_vyv.text, self.prihodi_vyv.text, self.razhodi_vyv.text,
                            self.opisanie_vyv.text, self.dr1_vyv.text, self.dr2_vyv.text)
                self.data_vyv.text = ''
                self.opisanie_vyv.text = ''
                self.prihodi_vyv.text = '0'
                self.razhodi_vyv.text = '0'
                self.data_vyv.background_color = (1, 1, 1, 1)
                self.prihodi_vyv.background_color = (1, 1, 1, 1)
                self.razhodi_vyv.background_color = (1, 1, 1, 1)
            except ValueError:
                greska_tekst = ''

                if not vjarna_data:
                    self.data_vyv.background_color = (1, 0, 0, 0.8)
                    greska_tekst += f'{self.data_vyv.text} <- е неправилен формат на дата. \n Моля пропавете го на ГГГГ–ММ–ДД !'
                else:
                    self.prihodi_vyv.background_color = (1, 0, 0, 0.8)
                    self.razhodi_vyv.background_color = (1, 0, 0, 0.8)
                    greska_tekst += f'{self.prihodi_vyv.text} или {self.razhodi_vyv.text} са неправилен формат. \n Моля въведете цифри!'

                ivalid = Ppo()
                ivalid.add_widget(Label(text=greska_tekst))
                ivalid.show_pop()

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect

            barcode_info = barcode.data.decode('utf-8-sig')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

            with open("posleden_barkod.dat", mode='w') as file:
                file.write(barcode_info)
            sk_barcode_info = barcode_info.split('*')

            self.data_vyv.text = sk_barcode_info[2]
            self.razhodi_vyv.text = sk_barcode_info[4]
            self.dr1_vyv.text = sk_barcode_info[0]
            self.dr2_vyv.text = sk_barcode_info[1]
        return frame

    def turn_on_camera(self):

        with open("posleden_barkod.dat", mode='w') as f:
            f.write('')

        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()

        while ret:
            with open("posleden_barkod.dat", mode='r') as file:
                fajl = file.read()

            ret, frame = camera.read()
            frame = self.read_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            if fajl:
                break
            if cv2.getWindowProperty('Barcode/QR code reader', 1) == -1:
                break

        camera.release()
        cv2.destroyAllWindows()


class Ppo(GridLayout):

    def __init__(self, **kwargs):
        super(Ppo, self).__init__(**kwargs)
        self.cols = 1

        self.add_widget(Label(text=""))

    def show_pop(self):

        popwindow = Popup(title='ГРЕШКА !!!', content=self, size_hint=(None, None), size=(300, 100))
        popwindow.open()


class Interfejs(App):

    def build(self):
        self.icon = 'engconv.ico'
        return Grid_to()


if __name__ == '__main__':

    Interfejs().run()

