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
    generate_authentication_options,
    verify_authentication_response,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    RegistrationCredential,
    UserVerificationRequirement,
    AuthenticationCredential,
)
from .serializers import UserSerializer

User = get_user_model()

RP_ID = "bioemtric-auth.herokuapp.com"
RP_NAME = "Webauthn Webauthn"
ORGIN = "https://bioemtric-auth.herokuapp.com"


# Create your views here.
"""
    1. Registration
    2. Authentcation

"""
class UserAPI(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    # registration options
    @action(detail=True, methods=['POST'])
    def registration(self, request, format=None):
        # data = json.loads(request.body)
        data = request.data
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
    
    # verify registration response
    @action(detail=True, methods=['POST'])
    def registration_verification(self, request, format=None):
        registration_verification = verify_registration_response(
            credential=RegistrationCredential.parse_raw(request.data),
            expected_challenge=base64url_to_bytes(
                "CeTWogmg0cchuiYuFrv8DXXdMZSIQRVZJOga_xayVVEcBj0Cw3y73yhD4FkGSe-RrP6hPJJAIm3LVien4hXELg"
            ),
            expected_origin=ORGIN,
            expected_rp_id=RP_ID,
            require_user_verification=True,
        )

        data = json.loads(registration_verification.json(indent=2))
        return Response(data, status=status.HTTP_200_OK)

    # authentication options
    @action(detail=True, methods=['POST'])
    def authentication(self, request, format=None):
        options = generate_authentication_options(
            rp_id=RP_ID,
            user_verification=UserVerificationRequirement.REQUIRED,
        )
        data = json.loads(options_to_json(options))
        return Response(data, status=status.HTTP_200_OK)

    # verify authentication
    @action(detail=True, methods=['POST'])
    def authentication_verification(self, request, format=None):
        authentication_verification = verify_authentication_response(
            credential=AuthenticationCredential.parse_raw(request.data),
            expected_challenge=base64url_to_bytes(
                "iPmAi1Pp1XL6oAgq3PWZtZPnZa1zFUDoGbaQ0_KvVG1lF2s3Rt_3o4uSzccy0tmcTIpTTT4BU1T-I4maavndjQ"
            ),
            expected_rp_id=RP_ID,
            expected_origin=ORGIN,
            credential_public_key=base64url_to_bytes(
                "pAEDAzkBACBZAQDfV20epzvQP-HtcdDpX-cGzdOxy73WQEvsU7Dnr9UWJophEfpngouvgnRLXaEUn_d8HGkp_HIx8rrpkx4BVs6X_B6ZjhLlezjIdJbLbVeb92BaEsmNn1HW2N9Xj2QM8cH-yx28_vCjf82ahQ9gyAr552Bn96G22n8jqFRQKdVpO-f-bvpvaP3IQ9F5LCX7CUaxptgbog1SFO6FI6ob5SlVVB00lVXsaYg8cIDZxCkkENkGiFPgwEaZ7995SCbiyCpUJbMqToLMgojPkAhWeyktu7TlK6UBWdJMHc3FPAIs0lH_2_2hKS-mGI1uZAFVAfW1X-mzKL0czUm2P1UlUox7IUMBAAE"
            ),
            credential_current_sign_count=0,
            require_user_verification=True,
        )
        data = json.loads(authentication_verification.json(indent=2))
        return Response(data, status=status.HTTP_200_OK)
    