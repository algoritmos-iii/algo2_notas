import sys
import itsdangerous
from src.config import AppConfig

config = AppConfig()
signer = itsdangerous.URLSafeSerializer(config.secret_key)

print(signer.dumps(int(sys.argv[1])))

