from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DF", "Defender"
        MIDFIELDER = "MF", "Midfielder"
        FORWARD = "FW", "Forward"

    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=Position.choices)
    current_club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transfer(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="transfers"
    )
    origin_club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="outgoing_transfers",
    )
    destination_club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="incoming_transfers"
    )
    transfer_date = models.DateField()
    transfer_fee = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["-transfer_date"]

    def __str__(self):
        origin = self.origin_club.name if self.origin_club else "Free Agent"
        return f"{self.player.name}: {origin} → {self.destination_club.name}"
