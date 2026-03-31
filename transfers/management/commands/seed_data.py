from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from transfers.models import Club, Player, Transfer


class Command(BaseCommand):
    help = "Seed the database with sample clubs, players, and transfers"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Clubs
        clubs_data = [
            {"name": "Real Madrid", "country": "Spain", "founded_year": 1902},
            {"name": "FC Barcelona", "country": "Spain", "founded_year": 1899},
            {"name": "Manchester United", "country": "England", "founded_year": 1878},
            {"name": "Bayern Munich", "country": "Germany", "founded_year": 1900},
            {"name": "Juventus", "country": "Italy", "founded_year": 1897},
            {"name": "Paris Saint-Germain", "country": "France", "founded_year": 1970},
            {"name": "Liverpool", "country": "England", "founded_year": 1892},
            {"name": "Santos FC", "country": "Brazil", "founded_year": 1912},
        ]

        clubs = {}
        for data in clubs_data:
            club, created = Club.objects.get_or_create(**data)
            clubs[club.name] = club
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: {club.name}")

        # Players
        players_data = [
            {
                "name": "Kylian Mbappé",
                "date_of_birth": date(1998, 12, 20),
                "nationality": "France",
                "position": "FW",
                "current_club": clubs["Real Madrid"],
            },
            {
                "name": "Erling Haaland",
                "date_of_birth": date(2000, 7, 21),
                "nationality": "Norway",
                "position": "FW",
                "current_club": clubs["Manchester United"],
            },
            {
                "name": "Pedri",
                "date_of_birth": date(2002, 11, 25),
                "nationality": "Spain",
                "position": "MF",
                "current_club": clubs["FC Barcelona"],
            },
            {
                "name": "Matthijs de Ligt",
                "date_of_birth": date(1999, 8, 12),
                "nationality": "Netherlands",
                "position": "DF",
                "current_club": clubs["Bayern Munich"],
            },
            {
                "name": "Gianluigi Donnarumma",
                "date_of_birth": date(1999, 2, 25),
                "nationality": "Italy",
                "position": "GK",
                "current_club": clubs["Paris Saint-Germain"],
            },
        ]

        players = {}
        for data in players_data:
            player, created = Player.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            players[player.name] = player
            status = "Created" if created else "Already exists"
            self.stdout.write(f"  {status}: {player.name}")

        # Transfers
        transfers_data = [
            {
                "player": players["Kylian Mbappé"],
                "origin_club": clubs["Paris Saint-Germain"],
                "destination_club": clubs["Real Madrid"],
                "transfer_date": date(2024, 7, 1),
                "transfer_fee": None,
            },
            {
                "player": players["Kylian Mbappé"],
                "origin_club": None,
                "destination_club": clubs["Paris Saint-Germain"],
                "transfer_date": date(2017, 8, 31),
                "transfer_fee": Decimal("180000000.00"),
            },
            {
                "player": players["Matthijs de Ligt"],
                "origin_club": clubs["Juventus"],
                "destination_club": clubs["Bayern Munich"],
                "transfer_date": date(2022, 7, 19),
                "transfer_fee": Decimal("67000000.00"),
            },
            {
                "player": players["Matthijs de Ligt"],
                "origin_club": None,
                "destination_club": clubs["Juventus"],
                "transfer_date": date(2019, 7, 18),
                "transfer_fee": Decimal("75000000.00"),
            },
            {
                "player": players["Gianluigi Donnarumma"],
                "origin_club": None,
                "destination_club": clubs["Paris Saint-Germain"],
                "transfer_date": date(2021, 7, 14),
                "transfer_fee": None,
            },
        ]

        for data in transfers_data:
            _, created = Transfer.objects.get_or_create(
                player=data["player"],
                transfer_date=data["transfer_date"],
                defaults=data,
            )
            status = "Created" if created else "Already exists"
            origin = data["origin_club"].name if data["origin_club"] else "Free Agent"
            self.stdout.write(
                f"  {status}: {data['player'].name} ({origin} → {data['destination_club'].name})"
            )

        self.stdout.write(self.style.SUCCESS("Seed data loaded successfully!"))
