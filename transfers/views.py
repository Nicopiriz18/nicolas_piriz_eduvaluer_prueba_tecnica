from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TransferFilter
from .models import Club, Player, Transfer
from .serializers import ClubSerializer, PlayerSerializer, TransferSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.select_related("current_club").all()
    serializer_class = PlayerSerializer

    @action(detail=True, methods=["get"])
    def transfers(self, request, pk=None):
        player = self.get_object()
        transfers = Transfer.objects.filter(player=player).select_related(
            "origin_club", "destination_club"
        )
        page = self.paginate_queryset(transfers)
        if page is not None:
            serializer = TransferSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data)


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.select_related(
        "player", "origin_club", "destination_club"
    ).all()
    serializer_class = TransferSerializer
    filterset_class = TransferFilter
    ordering_fields = ["transfer_date", "transfer_fee"]
