"""Domain models for client municipalities, public bodies and public officials."""

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

ibge_code_validator = RegexValidator(
    regex=r"^\d{7}$",
    message="O código IBGE deve conter exatamente 7 dígitos numéricos.",
)

acronym_validator = RegexValidator(
    regex=r"^[A-Z]{2,15}$",
    message=(
        "A sigla deve conter de 2 a 15 letras maiúsculas, sem espaços, "
        "acentos ou números (ex.: SEMED)."
    ),
)

phone_validator = RegexValidator(
    regex=r"^\(\d{2}\) \d{4,5}-\d{4}$",
    message="Informe o telefone no formato (99) 99999-9999 ou (99) 9999-9999.",
)


class TimeStampedModel(models.Model):
    """Abstract base model that tracks creation and update timestamps."""

    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        abstract = True


class Municipality(TimeStampedModel):
    """A client municipality served by the service provider."""

    class State(models.TextChoices):
        AC = "AC", "Acre"
        AL = "AL", "Alagoas"
        AP = "AP", "Amapá"
        AM = "AM", "Amazonas"
        BA = "BA", "Bahia"
        CE = "CE", "Ceará"
        DF = "DF", "Distrito Federal"
        ES = "ES", "Espírito Santo"
        GO = "GO", "Goiás"
        MA = "MA", "Maranhão"
        MT = "MT", "Mato Grosso"
        MS = "MS", "Mato Grosso do Sul"
        MG = "MG", "Minas Gerais"
        PA = "PA", "Pará"
        PB = "PB", "Paraíba"
        PR = "PR", "Paraná"
        PE = "PE", "Pernambuco"
        PI = "PI", "Piauí"
        RJ = "RJ", "Rio de Janeiro"
        RN = "RN", "Rio Grande do Norte"
        RS = "RS", "Rio Grande do Sul"
        RO = "RO", "Rondônia"
        RR = "RR", "Roraima"
        SC = "SC", "Santa Catarina"
        SP = "SP", "São Paulo"
        SE = "SE", "Sergipe"
        TO = "TO", "Tocantins"

    name = models.CharField("nome", max_length=100)
    state = models.CharField("UF", max_length=2, choices=State.choices)
    ibge_code = models.CharField(
        "código IBGE",
        max_length=7,
        unique=True,
        validators=[ibge_code_validator],
        error_messages={"unique": "Já existe um município com este código IBGE."},
        help_text="Código de 7 dígitos atribuído pelo IBGE ao município.",
    )

    class Meta:
        verbose_name = "município"
        verbose_name_plural = "municípios"
        ordering = ["name", "state"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "state"],
                name="unique_municipality_name_per_state",
                violation_error_message="Já existe um município com este nome nesta UF.",
            ),
        ]

    def __str__(self):
        return f"{self.name}/{self.state}"


class PublicBody(TimeStampedModel):
    """A public body (city hall, secretariat, etc.) belonging to a municipality."""

    class Kind(models.TextChoices):
        CITY_HALL = "city_hall", "Prefeitura"
        SECRETARIAT = "secretariat", "Secretaria"
        CITY_COUNCIL = "city_council", "Câmara Municipal"
        AUTARCHY = "autarchy", "Autarquia"
        FOUNDATION = "foundation", "Fundação"
        OTHER = "other", "Outro"

    municipality = models.ForeignKey(
        Municipality,
        verbose_name="município",
        on_delete=models.PROTECT,
        related_name="public_bodies",
    )
    name = models.CharField("nome", max_length=150)
    acronym = models.CharField(
        "sigla",
        max_length=15,
        blank=True,
        validators=[acronym_validator],
        help_text="Opcional. Use letras maiúsculas sem espaços (ex.: SEMED).",
    )
    kind = models.CharField("tipo", max_length=20, choices=Kind.choices)

    class Meta:
        verbose_name = "órgão público"
        verbose_name_plural = "órgãos públicos"
        ordering = ["municipality__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["municipality", "name"],
                name="unique_public_body_name_per_municipality",
                violation_error_message="Já existe um órgão com este nome neste município.",
            ),
            models.UniqueConstraint(
                fields=["municipality", "acronym"],
                condition=~Q(acronym=""),
                name="unique_public_body_acronym_per_municipality",
                violation_error_message="Já existe um órgão com esta sigla neste município.",
            ),
        ]

    def __str__(self):
        label = f"{self.name} ({self.acronym})" if self.acronym else self.name
        return f"{label} - {self.municipality}"


class Position(TimeStampedModel):
    """A position (job title) that public officials can hold."""

    name = models.CharField(
        "nome",
        max_length=100,
        unique=True,
        error_messages={"unique": "Já existe um cargo com este nome."},
    )

    class Meta:
        verbose_name = "cargo"
        verbose_name_plural = "cargos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PublicOfficial(TimeStampedModel):
    """A public official linked to a public body and holding a position."""

    name = models.CharField("nome", max_length=150)
    public_body = models.ForeignKey(
        PublicBody,
        verbose_name="órgão público",
        on_delete=models.PROTECT,
        related_name="public_officials",
    )
    position = models.ForeignKey(
        Position,
        verbose_name="cargo",
        on_delete=models.PROTECT,
        related_name="public_officials",
    )
    email = models.EmailField("e-mail", blank=True)
    phone = models.CharField(
        "telefone",
        max_length=15,
        blank=True,
        validators=[phone_validator],
        help_text="Formato: (99) 99999-9999 ou (99) 9999-9999.",
    )
    is_active = models.BooleanField(
        "ativo",
        default=True,
        help_text="Desmarque quando o agente deixar o cargo.",
    )

    class Meta:
        verbose_name = "agente público"
        verbose_name_plural = "agentes públicos"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.position}"
