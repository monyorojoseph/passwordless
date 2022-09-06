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

RP_ID = "monyorojoseph.herokuapp.com"
RP_NAME = "MJ co"

# Create your views here.
"""
    1. Registration

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
        pass
        # pregistration_verification = verify_registration_response(
        # credential=RegistrationCredential.parse_raw(
        #     """{
        #     "id": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
        #     "rawId": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
        #     "response": {
        #         "attestationObject": "o2NmbXRkbm9uZWdhdHRTdG10oGhhdXRoRGF0YVkBZ0mWDeWIDoxodDQXD2R2YFuP5K65ooYyx5lc87qDHZdjRQAAAAAAAAAAAAAAAAAAAAAAAAAAACBmggo_UlC8p2tiPVtNQ8nZ5NSxst4WS_5fnElA2viTq6QBAwM5AQAgWQEA31dtHqc70D_h7XHQ6V_nBs3Tscu91kBL7FOw56_VFiaKYRH6Z4KLr4J0S12hFJ_3fBxpKfxyMfK66ZMeAVbOl_wemY4S5Xs4yHSWy21Xm_dgWhLJjZ9R1tjfV49kDPHB_ssdvP7wo3_NmoUPYMgK-edgZ_ehttp_I6hUUCnVaTvn_m76b2j9yEPReSwl-wlGsabYG6INUhTuhSOqG-UpVVQdNJVV7GmIPHCA2cQpJBDZBohT4MBGme_feUgm4sgqVCWzKk6CzIKIz5AIVnspLbu05SulAVnSTB3NxTwCLNJR_9v9oSkvphiNbmQBVQH1tV_psyi9HM1Jtj9VJVKMeyFDAQAB",
        #         "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uY3JlYXRlIiwiY2hhbGxlbmdlIjoiQ2VUV29nbWcwY2NodWlZdUZydjhEWFhkTVpTSVFSVlpKT2dhX3hheVZWRWNCajBDdzN5NzN5aEQ0RmtHU2UtUnJQNmhQSkpBSW0zTFZpZW40aFhFTGciLCJvcmlnaW4iOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJjcm9zc09yaWdpbiI6ZmFsc2V9"
        #     },
        #     "type": "public-key",
        #     "clientExtensionResults": {},
        #     "transports": ["internal"]
        # }"""
        # ),
        # expected_challenge=base64url_to_bytes(
        #     "CeTWogmg0cchuiYuFrv8DXXdMZSIQRVZJOga_xayVVEcBj0Cw3y73yhD4FkGSe-RrP6hPJJAIm3LVien4hXELg"
        # ),
        # expected_origin="http://localhost:5000",
        # expected_rp_id="localhost",
        # require_user_verification=True,
    # )

    # authentication options
    @action(detail=True, methods=['POST'])
    def authentication(self, request, format=None):
        pass

    # verify authentication
    @action(detail=True, methods=['POST'])
    def authentication_verification(self, request, format=None):
        pass
    