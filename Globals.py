from source import University


class Globals:
    phystech = University("phystech")
    phystech.create_auditorium("202 HK", 250)
    phystech.create_auditorium("239 HK", 300)
    phystech.create_auditorium("123 ГК", 100)
    phystech.create_auditorium("525 ГК", 20)