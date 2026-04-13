import jwt
import time
import os
from pathlib import Path
from dotenv import load_dotenv

class GitHubAppDomain:
    def __init__(self):
        project_root = Path(__file__).parent.parent.parent
        env_path = project_root / ".env"
        load_dotenv(dotenv_path=env_path)

        self.app_id = os.getenv("APP_ID")
        self.installation_id = os.getenv("INSTALLATION_ID")
        self.pem_path = os.getenv("PRIVATE_KEY_PATH")

        self.pem_path = str(project_root / self.pem_path)

    def generate_jwt(self):
        with open(self.pem_path, "r", encoding="utf-8") as f:
            signing_key = f.read()

        now = int(time.time())
        # 严格遵循 GitHub 要求：exp 最大 600 秒，iat 提前 30 秒避免时钟偏差
        payload = {
            "iat": now - 30,
            "exp": now + 600,
            "iss": self.app_id
        }

        return jwt.encode(
            payload,
            signing_key,
            algorithm="RS256"
        )