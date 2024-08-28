import pytest
from tests import utils
from django.core.exceptions import ValidationError
from django.core.management import call_command

from links.models import Color


@pytest.mark.django_db(transaction=True)
class Test00ColorModel:
    """Тестирование логики модели Color"""

    def test_01_01_create_color(self, correct_color_data):
        color = Color.objects.create(
            name=correct_color_data['name'],
            color_hex=correct_color_data['color_hex']
        )

        assert color.id is not None, "Цвет не был создан, id должен быть не None."
        assert color.name == correct_color_data['name'], "Имя цвета не совпадает с ожидаемым."
        assert color.color_hex == correct_color_data['color_hex'], "Hex-код цвета не совпадает с ожидаемым."

    def test_01_02_create_color_and_check_idempotency(self, correct_color_data):
        color = Color.objects.create(
            name=correct_color_data['name'],
            color_hex=correct_color_data['color_hex']
        )

        assert color.id is not None, "Цвет не был создан, id должен быть не None."
        assert color.name == correct_color_data['name'], "Имя цвета не совпадает с ожидаемым."
        assert color.color_hex == correct_color_data['color_hex'], "Hex-код цвета не совпадает с ожидаемым."

        with pytest.raises(ValidationError) as e:
            color = Color.objects.create(
                name=correct_color_data['name'],
                color_hex=correct_color_data['color_hex']
            )

        assert e.type is ValidationError, "Нельзя создать такой же цвет."

    def test_01_03_create_color_with_empty_name(self, empty_color_name):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name=empty_color_name['name'],
                color_hex=empty_color_name['color_hex']
            )

        assert e.type is ValidationError, "Нельзя создать цвет с пустым именем."

    def test_01_04_create_color_with_empty_hex(self, empty_color_hex):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name=empty_color_hex['name'],
                color_hex=empty_color_hex['color_hex']
            )

        assert e.type is ValidationError, "Нельзя создать цвет без его HEX."

    def test_01_05_create_color_with_empty_fields(self, empty_color_fields):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name=empty_color_fields['name'],
                color_hex=empty_color_fields['color_hex']
            )

        assert e.type is ValidationError, 'Нельзя создать цвет без имени и HEX.'

    def test_01_06_create_color_len_restrict_for_name(self, very_long_color_name_over_limit):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name=very_long_color_name_over_limit['name'],
                color_hex=very_long_color_name_over_limit['color_hex']
            )

        assert e.type is ValidationError, "Нельзя создать цвет с именем, которое превышает лимит."

    def test_01_06_create_color_with_long_name_end_limit(self, very_long_color_name):
        color = Color.objects.create(
            name=very_long_color_name['name'],
            color_hex=very_long_color_name['color_hex']
        )

        assert color.id is not None, "Цвет не был создан, id должен быть не None."
        assert color.name == very_long_color_name['name'], "Имя цвета не совпадает с ожидаемым."
        assert color.color_hex == very_long_color_name['color_hex'], "Hex-код цвета не совпадает с ожидаемым."

    def test_01_06_create_color_with_short_name(self, very_short_color_name):
        color = Color.objects.create(
            name=very_short_color_name['name'],
            color_hex=very_short_color_name['color_hex']
        )

        assert color.id is not None, "Цвет не был создан, id должен быть не None."
        assert color.name == very_short_color_name['name'], "Имя цвета не совпадает с ожидаемым."
        assert color.color_hex == very_short_color_name['color_hex'], "Hex-код цвета не совпадает с ожидаемым."

    def test_01_06_create_color_without_name(self, color_without_name):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                color_hex=color_without_name['color_hex']
            )

        assert e.type is ValidationError, "Нельзя создать цвет без имени."

    def test_01_07_create_color_without_hex(self, color_without_hex):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name=color_without_hex['name'],
            )

        assert e.type is ValidationError, "Нельзя создать цвет без HEX."

    def test_01_08_create_color_with_short_hex(self, color_hex_short):
        color = Color.objects.create(
            name=color_hex_short['name'],
            color_hex=color_hex_short['color_hex']
        )

        assert color.id is not None, "Цвет не был создан, id должен быть не None."
        assert color.name == color_hex_short['name'], "Имя цвета не совпадает с ожидаемым."
        assert color.color_hex == color_hex_short['color_hex'], "Hex-код цвета не совпадает с ожидаемым."

    def test_01_09_create_color_with_wrong_hex(self):
        with pytest.raises(ValidationError) as e:
            Color.objects.create(
                name='Test Color',
                color_hex='SKIBIDI'
            )

        assert e.type is ValidationError, \
            (
                'Цвет не может создаться с HEX, '
                'который не соответствует правильному.'
            )


@pytest.mark.django_db(transaction=True)
class Test01ColorDjangoManageCommand:
    def test_01_01_run_command(self):
        colors_count_before = Color.objects.count()

        assert colors_count_before == 0, \
            "В базе перед запуском команды добавления цветов уже есть записи!"

        call_command("init_all_colors")

        colors_count_after = Color.objects.count()

        assert (colors_count_after != colors_count_before and
                colors_count_after == utils.count_colors_from_csv()), \
            "Ошибка при сравнении количества добавленных записей и нужного."

    def test_01_02_run_command_with_force_argument(self):
        call_command("init_all_colors")
        colors_count = Color.objects.count()

        assert colors_count != 0, "Цвета не были добавлены."

        call_command("init_all_colors", "--force")
        colors_count_force = Color.objects.count()

        assert colors_count_force == colors_count, \
            "Цвета не были удалены и добавлены вновь командой --force"

    def test_01_03_run_command_with_delete_colors_argument(self):
        call_command("init_all_colors")
        colors_count = Color.objects.count()

        assert colors_count != 0, "Цвета не были добавлены."

        call_command("init_all_colors", "--delete-colors")
        colors_count_after_delete = Color.objects.count()

        assert (colors_count_after_delete != colors_count and
                colors_count_after_delete == 0), \
            'Цвета не удалились из базы данных'
