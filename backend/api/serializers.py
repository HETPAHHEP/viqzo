from rest_framework.serializers import ModelSerializer
from links.models import ShortLink
from services.url_short_logic import LinkHash


class LinkReadSerializer(ModelSerializer):
    """Сериализатор для чтения ссылок"""

    class Meta:
        model = ShortLink
        fields = ['original_link', 'short_url', 'created_at']


class LinkWriteSerializer(ModelSerializer):
    """Сериализатор для записи ссылок"""

    class Meta:
        model = ShortLink
        fields = ['original_link']

    def create(self, validated_data):
        short_code = LinkHash().get_short_code()



    def to_representation(self, instance):
        created_link = LinkReadSerializer(instance=instance).data
        return created_link
