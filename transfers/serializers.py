from datetime import date

from django.db import transaction
from rest_framework import serializers

from .models import Club, Player, Transfer


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    current_club_name = serializers.StringRelatedField(
        source="current_club", read_only=True
    )

    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "date_of_birth",
            "nationality",
            "position",
            "current_club",
            "current_club_name",
        ]


class TransferSerializer(serializers.ModelSerializer):
    player_name = serializers.StringRelatedField(source="player", read_only=True)
    origin_club_name = serializers.StringRelatedField(
        source="origin_club", read_only=True
    )
    destination_club_name = serializers.StringRelatedField(
        source="destination_club", read_only=True
    )

    class Meta:
        model = Transfer
        fields = [
            "id",
            "player",
            "player_name",
            "origin_club",
            "origin_club_name",
            "destination_club",
            "destination_club_name",
            "transfer_date",
            "transfer_fee",
        ]

    def validate_transfer_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Transfer date cannot be in the future.")
        return value

    def validate(self, data):
        origin = data.get("origin_club")
        destination = data.get("destination_club")

        if origin and destination and origin == destination:
            raise serializers.ValidationError(
                {"destination_club": "Destination club must be different from origin club."}
            )

        player = data.get("player")
        if player and destination and player.current_club == destination:
            raise serializers.ValidationError(
                {"destination_club": "Player already belongs to this club."}
            )

        return data

    def create(self, validated_data):
        with transaction.atomic():
            transfer = super().create(validated_data)
            player = transfer.player
            player.current_club = transfer.destination_club
            player.save(update_fields=["current_club"])
        return transfer
