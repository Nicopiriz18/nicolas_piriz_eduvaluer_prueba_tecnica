from django_filters import rest_framework as filters

from .models import Transfer


class TransferFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="transfer_date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="transfer_date", lookup_expr="lte")
    fee_min = filters.NumberFilter(field_name="transfer_fee", lookup_expr="gte")
    fee_max = filters.NumberFilter(field_name="transfer_fee", lookup_expr="lte")

    class Meta:
        model = Transfer
        fields = ["player", "origin_club", "destination_club"]
