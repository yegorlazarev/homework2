class Tonel():
    def __init__(self, coordinates: tuple[float, float, float], type_: str):
        if type_ not in ('трапецеидальная', 'арочная'):
            raise ValueError('неверный тип крепей. Могут быть только "трапецеидальная" или "арочная"')
        self.coordinates = coordinates
        self.type_ = type_

    def get_coors(self):
        return self.coordinates


class Image:
    def __init__(self, image: list[float]):
        self.image = image

    pass


class Shtolnya():
    def __init__(self, tonels: list[Tonel]):
        self.tonels = tonels

    def add_tonnels(self, tonels: list[Tonel]):
        self.tonels += tonels


class Track():
    def __init__(self, tonels: list[Tonel]):
        if tonels[0].get_coors() != (0, 0, 0):
            raise ValueError('Путь должен начинатся с тоннеля с координатами (0,0,0). Проверьте себя!')
        else:
            self.tonels = tonels

    def track_full(self):
        return [i.get_coors() for i in self.tonels]


class Machine():
    def __init__(self, on_base: bool, track: Track, current_position: tuple[float, float, float]):
        self.on_base = on_base
        self.track_coors = None if on_base else track.track_full()
        self.current_position = current_position

    def update_position(self, new_position: tuple[float, float, float]):
        self.current_position = new_position


class Bur(Machine):
    def mine(self):
        pass


class Cartomachine(Machine):
    def make_cartography(self) -> Image:
        pass


class Revisor(Machine):
    def __init__(self, on_base: bool, track: Track, current_position: tuple[float, float, float]):
        super().__init__(on_base, track, current_position)
        self.track = track  # может быть важен тип крепы при оценки поэтому сохраняем его

    def take_photo(self) -> Image:
        pass

    def assess(self) -> float:
        pass

    def assess_route(self) -> tuple[dict[tuple[float, float, float], Image], dict[tuple[float, float, float], float]]:
        photos = {}
        assessment = {}
        for i in self.track_coors:
            photos[i] = self.take_photo()
            assessment[i] = self.assess()
        return photos, assessment


class Controller():
    def __init__(self, shtolnya: Shtolnya, burs: list[Bur], cartomachines: list[Cartomachine], revisors: list[Revisor]):
        self.shtolnya = shtolnya
        self.burs = burs
        self.cartomachines = cartomachines
        self.revisors = revisors

    def select_on_track(self) -> tuple[list[Bur], list[Cartomachine], list[Revisor]]:
        return [i for i in self.burs if not i.on_base], [j for j in self.cartomachines if not j.on_base], [k for k in
                                                                                                           self.revisors
                                                                                                           if
                                                                                                           not k.on_base]

    def send_to_base(self, burs: list[Bur], cartomachines: list[Cartomachine], revisors: list[Revisor]) -> None:
        __machines = burs + cartomachines + revisors
        for machine in __machines:
            machine.track_coors = None
            machine.on_base = True
            machine.current_position = (0, 0, 0)

    def select_on_base(self) -> tuple[list[Bur], list[Cartomachine], list[Revisor]]:
        return [i for i in self.burs if i.on_base], [j for j in self.cartomachines if j.on_base], [k for k in
                                                                                                   self.revisors if
                                                                                                   k.on_base]

    def send_to_tracks(self, burs: list[Bur], cartomachines: list[Cartomachine], revisors: list[Revisor],
                       burs_tracks: list[Track], cartomachines_tracks: list[Track],
                       revisors_tracks: list[Track]) -> None:
        if len(burs_tracks) != len(burs) or len(cartomachines_tracks) != len(cartomachines) or len(revisors) != len(
                revisors_tracks):
            raise ValueError('Количество путей не соответствует количеству машин')
        for machine, track in zip(burs + cartomachines + revisors,
                                  burs_tracks + cartomachines_tracks + revisors_tracks):
            machine.on_base = False
            machine.track_coors = track.track_full()
