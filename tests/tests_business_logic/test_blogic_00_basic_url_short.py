import pytest
import re

from backend.api.services.url_short_logic import LinkHash, LinkIDZeroError
from backend.core.enums import Limits


class Test00BasicURLShort:
    def test_01_get_short_code_for_url(self):
        assert type(LinkHash().get_short_code()) is str, (
            'Короткий код для url не является строкой'
        )

    def test_02_01_valid_alphabet_of_generated_code(self):
        regex = r'^[a-zA-Z0-9]+$'
        code = LinkHash().get_short_code()
        assert re.match(regex, code), (
            f'Код не соответствует используемому алфавиту Base62'
        )

    def test_02_02_check_code_len(self):
        limit = Limits.MAX_LEN_LINK_SHORT_CODE
        code_len = len(LinkHash().get_short_code())

        assert code_len == limit, (
                f'Короткий код длиной {code_len} не соответствует нужной длине {limit}'
            )

    def test_03_01_expected_result_of_generated_code(self):
        number_process = int('1' * 13)
        expected_code = 'PZ6NMPx'
        result_hashing = LinkHash()._to_base_62(number_process)

        assert expected_code == result_hashing, (
            f'Результат получения короткого кода из числа {number_process} '
            f'Не является корректным -> expected: {expected_code} result: {result_hashing}'
        )

    def test_03_02_idempotency_of_generated_code(self):
        number_process = int('1' * 13)
        expected_code = 'PZ6NMPx'
        result1 = LinkHash()._to_base_62(number_process)
        result2 = LinkHash()._to_base_62(number_process)

        assert expected_code == result1 == result2, (
            f'Преобразование числа в короткий код не идемпотентно -> '
            f'expected: {expected_code} result1: {result1} result2: {result2}'
        )

    def test_04_restrictions_for_generated_code(self):
        with pytest.raises(LinkIDZeroError):
            LinkHash()._to_base_62(0)
            LinkHash()._to_base_62(-1000)

        with pytest.raises(TypeError):
            LinkHash()._to_base_62('abcdefteststringsrtlalalal')
