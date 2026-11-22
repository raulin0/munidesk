import pytest
from django.core.exceptions import ValidationError

from municipalities.models import Municipality, PublicBody, PublicOfficial

pytestmark = pytest.mark.django_db


class TestMunicipality:
    def test_str_shows_name_and_state(self, municipality):
        assert str(municipality) == "Campinas/SP"

    @pytest.mark.parametrize("ibge_code", ["350950", "35095021", "35O9502"])
    def test_rejects_invalid_ibge_code(self, ibge_code):
        municipality = Municipality(name="Sumaré", state="SP", ibge_code=ibge_code)

        with pytest.raises(ValidationError) as exc:
            municipality.full_clean()

        assert "ibge_code" in exc.value.message_dict

    def test_rejects_duplicate_name_in_same_state(self, municipality):
        duplicate = Municipality(name="Campinas", state="SP", ibge_code="3509503")

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "Já existe um município com este nome nesta UF." in exc.value.messages

    def test_allows_same_name_in_different_states(self, municipality):
        Municipality(name="Campinas", state="RS", ibge_code="4304507").full_clean()


class TestPublicBody:
    def test_acronym_is_optional(self, municipality):
        public_body = PublicBody(
            municipality=municipality,
            name="Prefeitura Municipal de Campinas",
            kind=PublicBody.Kind.CITY_HALL,
        )

        public_body.full_clean()

    @pytest.mark.parametrize("acronym", ["semed", "SE MED", "SEMÉD", "SEMED1", "S"])
    def test_rejects_acronym_outside_municipal_pattern(self, municipality, acronym):
        public_body = PublicBody(
            municipality=municipality,
            name="Secretaria Municipal de Saúde",
            acronym=acronym,
            kind=PublicBody.Kind.SECRETARIAT,
        )

        with pytest.raises(ValidationError) as exc:
            public_body.full_clean()

        assert "acronym" in exc.value.message_dict

    def test_rejects_duplicate_acronym_in_same_municipality(self, public_body):
        duplicate = PublicBody(
            municipality=public_body.municipality,
            name="Secretaria Municipal de Esportes",
            acronym="SEMED",
            kind=PublicBody.Kind.SECRETARIAT,
        )

        with pytest.raises(ValidationError) as exc:
            duplicate.full_clean()

        assert "Já existe um órgão com esta sigla neste município." in exc.value.messages

    def test_allows_many_bodies_without_acronym(self, municipality):
        for name in ["Câmara Municipal de Campinas", "Fundação José Pedro de Oliveira"]:
            PublicBody.objects.create(
                municipality=municipality,
                name=name,
                kind=PublicBody.Kind.OTHER,
            )

        assert PublicBody.objects.filter(acronym="").count() == 2

    def test_str_includes_acronym_when_present(self, public_body):
        assert str(public_body) == "Secretaria Municipal de Educação (SEMED) - Campinas/SP"


class TestPublicOfficial:
    def test_is_active_by_default(self, public_official):
        assert public_official.is_active is True

    def test_rejects_invalid_phone(self, public_body, position):
        official = PublicOfficial(
            name="João Carlos Ferreira",
            public_body=public_body,
            position=position,
            phone="19998765432",
        )

        with pytest.raises(ValidationError) as exc:
            official.full_clean()

        assert "phone" in exc.value.message_dict

    def test_str_shows_name_and_position(self, public_official):
        assert str(public_official) == (
            "Maria Aparecida dos Santos - Secretário Municipal de Educação"
        )
