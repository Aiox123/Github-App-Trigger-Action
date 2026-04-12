import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from src.github_app import GitHubApp

# 同样手动加载.env，双重保险
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

class ActionController:
    def __init__(self):
        self.app = GitHubApp()
        self.token = self.app.get_installation_token()
        self.repo = os.getenv("REPO")
        self.event_type = os.getenv("EVENT_TYPE")

    def trigger_action(self):
        url = f"https://api.github.com/repos/{self.repo}/dispatches"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }
        payload = {"event_type": self.event_type}
        resp = requests.post(url, json=payload, headers=headers)
        print(f"[DEBUG] 触发Action状态码：{resp.status_code}")
        return resp.status_code in (200, 204)