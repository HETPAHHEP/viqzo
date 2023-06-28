from django.core.validators import RegexValidator


class ShortURLValidator(RegexValidator):
    """Validator for short link code"""
    regex = r'^[a-zA-Z0-9]{6}$'
    message = _('Link short code is invalid')
    code = 'short_url_error'
