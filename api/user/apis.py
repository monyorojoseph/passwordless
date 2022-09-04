import json
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
    RegistrationCredential,
)
from .serializers import UserSerializer

User = get_user_model()

RP_ID = "http://localhost:8000/"
RP_NAME = "Example Co"

# Create your views here.
"""
    1. Registration

"""
class UserAPI(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    @action(detail=True, methods=['POST'])
    def registration(self, request, format=None):
        data = json.loads(request.body)
        user = User(email=data['email'], username=data['username'])
        user.save()
        options = generate_registration_options(
            rp_id=RP_ID,
            rp_name=RP_NAME,
            user_id=str(user.id),
            user_name=user.username,
            attestation=AttestationConveyancePreference.DIRECT,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                resident_key=ResidentKeyRequirement.REQUIRED,
            ),
            supported_pub_key_algs=[COSEAlgorithmIdentifier.ECDSA_SHA_512],
        )
        data = json.loads(options_to_json(options))
        return Response(data, status=status.HTTP_201_CREATED)