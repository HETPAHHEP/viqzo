class LinkIDZeroError(Exception):
    def __str__(self):
        return "link_id должен быть положительным целым числом"
