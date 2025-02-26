class Champion:
    def __init__(
        self,
        lane: str,
        name: str,
        win_rate: float,
        pick_rate: float,
        ban_rate: float,
    ):
        self.__lane = lane
        self.__name = name
        self.__win_rate = win_rate
        self.__pick_rate = pick_rate
        self.__ban_rate = ban_rate
        self.__adjusted_win_rate = 0.0
        self.__tier = ""

    @property
    def lane(self) -> str:
        return self.__lane

    @property
    def name(self) -> str:
        return self.__name

    @property
    def win_rate(self) -> float:
        return self.__win_rate

    @property
    def pick_rate(self) -> float:
        return self.__pick_rate

    @property
    def ban_rate(self) -> float:
        return self.__ban_rate

    @property
    def adjusted_win_rate(self) -> float:
        return self.__adjusted_win_rate

    @adjusted_win_rate.setter
    def adjusted_win_rate(self, value: float) -> None:
        self.__adjusted_win_rate = value

    @property
    def tier(self) -> str:
        return self.__tier

    @tier.setter
    def tier(self, value: str) -> None:
        self.__tier = value

    def to_csv_row(self) -> list[str | float]:
        return [
            self.__lane,
            self.__name,
            self.__win_rate,
            self.__pick_rate,
            self.__ban_rate,
            self.__adjusted_win_rate,
            self.__tier,
        ]
