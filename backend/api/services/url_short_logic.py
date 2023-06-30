import uuid

from .services_exceptions import LinkIDZeroError


class LinkHash:
    """
    Генерация короткой ссылки по переводу id оригинальной ссылки в Base62.

    Фиксированная длина всех ссылок определяется code_fix_len
    """

    def __init__(self):
        # перемешанный алфавит с 0-9 и в английскими буквами нижнего и верхнего регистра
        self.alphabet = '0GTWYahl4C1Dq2evKiNPJdwfLxAsH9t8E5Z3RISyUuzQVk7rjFn6mpgbBXOcoM'
        self.base_len = len(self.alphabet)
        self.code_fix_len = 7

    @staticmethod
    def _get_id_for_link() -> int:
        """Получения случайного id для ссылки"""
        random_uuid = uuid.uuid4().int

        return random_uuid

    def _to_base_62(self, link_id: int) -> str:
        """Получение сокращенного кода ссылки.

        :param link_id: Id для ассоциации со ссылкой
        :returns short_code: перевод id в base62
        """

        if link_id <= 0:
            raise LinkIDZeroError

        short_code = ''

        while link_id > 0:
            link_id, remainder = divmod(link_id, self.base_len)
            short_code += self.alphabet[remainder]

        # Укорачиваем код для использования в ссылке
        return short_code[self.code_fix_len - 1::-1]

    def get_short_code(self) -> str:
        random_id = self._get_id_for_link()
        short_code = self._to_base_62(random_id)

        return short_code


if __name__ == '__main__':
    # for manual test
    hash_for_link = LinkHash()
    print(hash_for_link.get_short_code())
