from django.utils.functional import cached_property
from django.core.paginator import Paginator


class Paginator(Paginator):
    @cached_property
    def count(self):
        return 9999999999
