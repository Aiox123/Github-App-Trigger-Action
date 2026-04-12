import jwt
import time
import requests
from dotenv import load_dotenv
import os
from pathlib import Path  # 新增，用于定位.env文件

# 1. 自动定位项目根目录的.env文件，无论从哪里运行都能找到
project_root = Path(__file__).parent.parent  # src的父目录就是rovo根目录
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)  # 手动指定.env路径，100%能加载到

class GitHubApp:
    def __init__(self):
        self.app_id = os.getenv("APP_ID")
        self.installation_id = os.getenv("INSTALLATION_ID")
        self.pem_path = os.getenv("PRIVATE_KEY_PATH")
        
        # 新增：打印调试信息，确认变量是否正确读取
        print(f"[DEBUG] APP_ID: {self.app_id}")
        print(f"[DEBUG] INSTALLATION_ID: {self.installation_id}")
        print(f"[DEBUG] PEM_PATH: {self.pem_path}")
        
        # 新增：参数校验，提前发现问题
        if not all([self.app_id, self.installation_id, self.pem_path]):
            raise ValueError("❌ 环境变量读取失败，请检查.env文件和路径！")
        
        # 把相对路径转为绝对路径，彻底解决Windows路径问题
        self.pem_path = str(project_root / self.pem_path)
        print(f"[DEBUG] 绝对路径PEM_PATH: {self.pem_path}")
        
        self.signing_key = self._load_pem()

    def _load_pem(self):
        # 新增：校验文件是否存在
        if not os.path.exists(self.pem_path):
            raise FileNotFoundError(f"❌ 私钥文件不存在！路径：{self.pem_path}")
        
        with open(self.pem_path, "r", encoding="utf-8") as f:
            return f.read()

    def generate_jwt(self):
        payload = {
            "iat": int(time.time()) - 60,
            "exp": int(time.time()) + 600,
            "iss": self.app_id
        }
        return jwt.encode(payload, self.signing_key, algorithm="RS256")

    def get_installation_token(self):
        jwt_token = self.generate_jwt()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json"
        }
        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        resp = requests.post(url, headers=headers)
        # 新增：API响应校验
        if resp.status_code != 201:
            raise Exception(f"❌ 获取安装令牌失败！状态码：{resp.status_code}，响应：{resp.text}")
        return resp.json()["token"]