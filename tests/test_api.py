import pytest
from rest_framework.test import APIClient

from municipalities.models import Municipality, PublicBody

pytestmark = pytest.mark.django_db


class TestAuthentication:
    @pytest.mark.parametrize(
        "url",
        [
            "/api/municipalities/",
            "/api/public-bodies/",
            "/api/positions/",
            "/api/public-officials/",
        ],
    )
    def test_anonymous_requests_are_rejected(self, url):
        response = APIClient().get(url)

        assert response.status_code == 403


class TestMunicipalityEndpoints:
    def test_lists_municipalities(self, api_client, municipality):
        response = api_client.get("/api/municipalities/")

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Campinas"

    def test_creates_municipality(self, api_client):
        payload = {"name": "Ribeirão Preto", "state": "SP", "ibge_code": "3543402"}

        response = api_client.post("/api/municipalities/", payload)

        assert response.status_code == 201
        assert Municipality.objects.filter(ibge_code="3543402").exists()

    def test_rejects_duplicate_name_in_same_state(self, api_client, municipality):
        payload = {"name": "Campinas", "state": "SP", "ibge_code": "3509503"}

        response = api_client.post("/api/municipalities/", payload)

        assert response.status_code == 400
        assert response.data["non_field_errors"] == [
            "Já existe um município com este nome nesta UF."
        ]

    def test_returns_conflict_when_deleting_municipality_with_bodies(self, api_client, public_body):
        response = api_client.delete(f"/api/municipalities/{public_body.municipality_id}/")

        assert response.status_code == 409
        assert Municipality.objects.filter(pk=public_body.municipality_id).exists()


class TestPublicBodyEndpoints:
    def test_creates_public_body_without_acronym(self, api_client, municipality):
        payload = {
            "municipality": municipality.pk,
            "name": "Prefeitura Municipal de Campinas",
            "kind": "city_hall",
        }

        response = api_client.post("/api/public-bodies/", payload)

        assert response.status_code == 201
        assert response.data["acronym"] == ""

    def test_rejects_acronym_outside_municipal_pattern(self, api_client, municipality):
        payload = {
            "municipality": municipality.pk,
            "name": "Secretaria Municipal de Saúde",
            "acronym": "Sec. Saúde",
            "kind": "secretariat",
        }

        response = api_client.post("/api/public-bodies/", payload)

        assert response.status_code == 400
        assert response.data["acronym"] == [
            "A sigla deve conter de 2 a 15 letras maiúsculas, sem espaços, "
            "acentos ou números (ex.: SEMED)."
        ]

    def test_rejects_duplicate_acronym_in_same_municipality(self, api_client, public_body):
        payload = {
            "municipality": public_body.municipality_id,
            "name": "Secretaria Municipal de Esportes",
            "acronym": "SEMED",
            "kind": "secretariat",
        }

        response = api_client.post("/api/public-bodies/", payload)

        assert response.status_code == 400
        assert response.data["non_field_errors"] == [
            "Já existe um órgão com esta sigla neste município."
        ]
        assert PublicBody.objects.filter(acronym="SEMED").count() == 1

    def test_rejects_unknown_kind(self, api_client, municipality):
        payload = {
            "municipality": municipality.pk,
            "name": "Secretaria Municipal de Obras",
            "kind": "ministry",
        }

        response = api_client.post("/api/public-bodies/", payload)

        assert response.status_code == 400
        assert "kind" in response.data


class TestPositionEndpoints:
    def test_rejects_duplicate_position(self, api_client, position):
        response = api_client.post("/api/positions/", {"name": "Secretário Municipal de Educação"})

        assert response.status_code == 400
        assert response.data["name"] == ["Já existe um cargo com este nome."]


class TestPublicOfficialEndpoints:
    def test_creates_public_official(self, api_client, public_body, position):
        payload = {
            "name": "José Roberto Almeida",
            "public_body": public_body.pk,
            "position": position.pk,
            "email": "jose.almeida@campinas.sp.gov.br",
            "phone": "(19) 3234-5678",
        }

        response = api_client.post("/api/public-officials/", payload)

        assert response.status_code == 201
        assert response.data["is_active"] is True

    def test_deactivates_public_official(self, api_client, public_official):
        response = api_client.patch(
            f"/api/public-officials/{public_official.pk}/", {"is_active": False}
        )

        assert response.status_code == 200
        public_official.refresh_from_db()
        assert public_official.is_active is False

    def test_deletes_public_official(self, api_client, public_official):
        response = api_client.delete(f"/api/public-officials/{public_official.pk}/")

        assert response.status_code == 204
