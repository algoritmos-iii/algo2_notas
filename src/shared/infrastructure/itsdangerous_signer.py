from typing import Any
import itsdangerous
from ..domain.signer_interface import SignerInterface, BadData


class ItsDangerousSigner(SignerInterface):
    def __init__(self, secret_key: str) -> None:
        self._signer = itsdangerous.URLSafeSerializer(secret_key)

    def sign(self, data: str) -> str:
        return self._signer.dumps(data)

    def unsign(self, signed_data: str) -> Any:
        try:
            return self._signer.loads(signed_data)
        except itsdangerous.BadData:
            raise BadData(signed_data)
