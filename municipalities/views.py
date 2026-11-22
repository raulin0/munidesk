from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Municipality, Position, PublicBody, PublicOfficial
from .serializers import (
    MunicipalitySerializer,
    PositionSerializer,
    PublicBodySerializer,
    PublicOfficialSerializer,
)


class ProtectedDeleteMixin:
    """Return 409 Conflict instead of a server error when related records exist."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    "detail": (
                        "Não é possível excluir este registro porque existem "
                        "outros registros vinculados a ele."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )


class MunicipalityViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class PublicBodyViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = PublicBody.objects.select_related("municipality")
    serializer_class = PublicBodySerializer


class PositionViewSet(ProtectedDeleteMixin, viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PublicOfficialViewSet(viewsets.ModelViewSet):
    queryset = PublicOfficial.objects.select_related("public_body", "position")
    serializer_class = PublicOfficialSerializer
