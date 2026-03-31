from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Club, Player, Transfer


class ClubAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.club = Club.objects.create(
            name="Test FC", country="Uruguay", founded_year=1900
        )

    def test_list_clubs(self):
        response = self.client.get("/api/clubs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_club(self):
        response = self.client.post(
            "/api/clubs/",
            {"name": "New Club", "country": "Argentina", "founded_year": 1950},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unique_club_name(self):
        response = self.client.post(
            "/api/clubs/",
            {"name": "Test FC", "country": "Brazil", "founded_year": 2000},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PlayerAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.club = Club.objects.create(
            name="Test FC", country="Uruguay", founded_year=1900
        )
        self.player = Player.objects.create(
            name="Test Player",
            date_of_birth=date(1995, 1, 1),
            nationality="Uruguay",
            position="FW",
            current_club=self.club,
        )

    def test_list_players(self):
        response = self.client.get("/api/players/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_player(self):
        response = self.client.post(
            "/api/players/",
            {
                "name": "New Player",
                "date_of_birth": "2000-05-15",
                "nationality": "Brazil",
                "position": "MF",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_player_transfers_endpoint(self):
        response = self.client.get(f"/api/players/{self.player.id}/transfers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransferAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.club_a = Club.objects.create(
            name="Club A", country="Spain", founded_year=1900
        )
        self.club_b = Club.objects.create(
            name="Club B", country="England", founded_year=1890
        )
        self.player = Player.objects.create(
            name="Transfer Player",
            date_of_birth=date(1998, 3, 10),
            nationality="France",
            position="FW",
            current_club=self.club_a,
        )

    def test_create_transfer(self):
        response = self.client.post(
            "/api/transfers/",
            {
                "player": self.player.id,
                "origin_club": self.club_a.id,
                "destination_club": self.club_b.id,
                "transfer_date": "2024-07-01",
                "transfer_fee": "50000000.00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transfer_same_origin_destination(self):
        response = self.client.post(
            "/api/transfers/",
            {
                "player": self.player.id,
                "origin_club": self.club_a.id,
                "destination_club": self.club_a.id,
                "transfer_date": "2024-07-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_future_date(self):
        future = date.today() + timedelta(days=30)
        response = self.client.post(
            "/api/transfers/",
            {
                "player": self.player.id,
                "origin_club": self.club_a.id,
                "destination_club": self.club_b.id,
                "transfer_date": future.isoformat(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_to_current_club(self):
        response = self.client.post(
            "/api/transfers/",
            {
                "player": self.player.id,
                "origin_club": self.club_b.id,
                "destination_club": self.club_a.id,
                "transfer_date": "2024-07-01",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_transfers(self):
        response = self.client.get("/api/transfers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_transfers_by_player(self):
        Transfer.objects.create(
            player=self.player,
            origin_club=self.club_a,
            destination_club=self.club_b,
            transfer_date=date(2024, 1, 1),
            transfer_fee=Decimal("1000000"),
        )
        response = self.client.get(f"/api/transfers/?player={self.player.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
