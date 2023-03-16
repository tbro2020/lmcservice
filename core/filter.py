import django_filters


class AdvanceFilterSet(django_filters.FilterSet):
    created = django_filters.DateFromToRangeFilter(
        label='Created',
        widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd'}))


def filterset_factory(model, fields="__all__"):
    meta = type(str("Meta"), (object,), {"model": model, "fields": fields})
    filterset = type(
        str("%sFilterSet" % model._meta.object_name), (AdvanceFilterSet,), {"Meta": meta}
    )
    return filterset
