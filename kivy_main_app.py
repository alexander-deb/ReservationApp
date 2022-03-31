from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
import datetime
from Globals import Globals



class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        self.date = datetime.date.today()
        self.time1 = datetime.time(hour=13, minute=30)
        self.time2 = datetime.time(hour=15, minute=0)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_file('Reservation.kv')


    def on_cancel(self, instance, time):
        pass

    def show_time_picker1(self):
        default_time = datetime.datetime.strptime("4:20:00", '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_time_from)
        time_dialog.open()

    def show_time_picker2(self):
        default_time = datetime.datetime.strptime("4:20:00", '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(default_time)
        time_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_time_to)
        time_dialog.open()

    def on_date_save(self, instance, value, date_range):
        date_value = datetime.datetime.strptime(str(value), "%Y-%m-%d")
        date_value_eu = date_value.strftime("%d.%m.%Y")
        self.date = value

    def on_time_from(self, instance, time):
        MDApp.get_running_app().root.ids['picker1'].text = time.strftime("%H:%M:%S")
        self.time1 = time

    def on_time_to(self, instance, time):
        MDApp.get_running_app().root.ids['picker2'].text = time.strftime("%H:%M:%S")
        self.time2 = time


    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_cancel=self.on_cancel, on_save=self.on_date_save)
        date_dialog.open()

    def search_rooms(self):
        '''
        Запуск поиска подходящих аудиторий
        :return:
        '''
        MDApp.get_running_app().root.ids['box'].clear_widgets()
        try:
            self.size = int(MDApp.get_running_app().root.ids['size'].text)
        except:
            self.size = 0

        self.list_of_rooms = Globals.phystech.recommendation(self.size, self.date, self.time1, self.time2)
        i = 0
        if len(self.list_of_rooms) > 0:
            for room in self.list_of_rooms:
                i += 1
                MDApp.get_running_app().root.ids['box'].add_widget(
                    MDRaisedButton(text=f"{i}. {room.name}.\n Вместимость: {room.size}", size_hint=(1,1), padding=(10, 10), on_release=self.choose))
        else:
            MDApp.get_running_app().root.ids['box'].add_widget(MDLabel(text="Аудиторий не найдено", pos_hint={'center_x': .9, 'center_y': .9}))


    def create_room(self):
        '''
        Непосредственное создание обьекта аудитории
        :return:
        '''
        try:
            new_name = MDApp.get_running_app().root.ids['name_of_aud'].text
            new_size = int(MDApp.get_running_app().root.ids['size_of_aud'].text)
            Globals.phystech.create_auditorium(new_name, new_size)
        except:
            pass

    def choose(self, instance):
        '''
        Срабатывает в момент нажатия на кнопку для выбора аудитории
        :param instance: instance of the button
        :return: None
        '''
        if self.list_of_rooms[int(instance.text.split()[0][:-1])-1].reserve(self.date, self.time1, self.time2) != "200 OK":
            MDApp.get_running_app().root.ids['box'].clear_widgets()
            MDApp.get_running_app().root.ids['box'].add_widget(MDLabel(
                text="Ошибка! Вы уже забронировали эту аудиторию на данное время.\n Чтобы выбрать другую аудиторию, нажмите поиск еще раз.",
                pos_hint={'center_x': .8, 'center_y': 1}
            ))
