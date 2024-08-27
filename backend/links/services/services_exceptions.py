class LinkIDZeroError(Exception):
    def __str__(self):
        return "link_id должен быть положительным целым числом"


class ShortCodeError(Exception):
    def __str__(self):
        return (
            "Сгенерированный short code не "
            "соответствует регулярному выражению"
        )
