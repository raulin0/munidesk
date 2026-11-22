import pytest

from municipalities.models import Municipality, Position, PublicBody, PublicOfficial


@pytest.fixture
def municipality(db):
    return Municipality.objects.create(
        name="Campinas",
        state=Municipality.State.SP,
        ibge_code="3509502",
    )


@pytest.fixture
def public_body(municipality):
    return PublicBody.objects.create(
        municipality=municipality,
        name="Secretaria Municipal de Educação",
        acronym="SEMED",
        kind=PublicBody.Kind.SECRETARIAT,
    )


@pytest.fixture
def position(db):
    return Position.objects.create(name="Secretário Municipal de Educação")


@pytest.fixture
def public_official(public_body, position):
    return PublicOfficial.objects.create(
        name="Maria Aparecida dos Santos",
        public_body=public_body,
        position=position,
        email="maria.santos@campinas.sp.gov.br",
        phone="(19) 99876-5432",
    )
