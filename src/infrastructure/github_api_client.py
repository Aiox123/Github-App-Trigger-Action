import requests
from src.common.logger import get_logger

class GitHubApiClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.logger = get_logger(__name__)

    def get_installation_token(self, jwt_token, installation_id):
        url = f"{self.base_url}/app/installations/{installation_id}/access_tokens"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        resp = requests.post(url, headers=headers)
        
        # ========== 加错误打印 ==========
        self.logger.info(f"GitHub 返回状态码: {resp.status_code}")
        self.logger.info(f"GitHub 返回内容: {resp.json()}")
        # ===============================
        
        if resp.status_code != 201:
            self.logger.error(f"获取安装令牌失败: {resp.json().get('message', '未知错误')}")
            raise Exception(f"获取安装令牌失败: {resp.json().get('message', '未知错误')}")
        
        return resp.json()["token"]

    def trigger_create_issue(self, token, repo, title, body):
        url = f"{self.base_url}/repos/{repo}/dispatches"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "event_type": "create-issue",
            "client_payload": {
                "title": title,
                "body": body
            }
        }
        resp = requests.post(url, json=payload, headers=headers)
        return resp.status_code