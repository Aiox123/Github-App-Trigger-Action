# 修复：把项目根目录加入 Python 路径
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

# 正常导入
from src.application.issue_service import IssueService
from dotenv import load_dotenv
import os
from src.common.logger import get_logger

def main():
    # 加载环境变量
    project_root = Path(__file__).parent.parent.parent
    load_dotenv(dotenv_path=project_root / ".env")

    repo = os.getenv("REPO")
    logger = get_logger(__name__)

    # =======================
    # ✅ 在这里写 Issue 内容
    # =======================
    issue_title = "🔥 GitHub App 触发 - 自动创建 Issue"
    issue_body = """
这条 Issue 通过 DDD 架构项目远程触发！
项目：Github-App-Trigger-Action
状态：执行成功 ✅
"""

    # 业务逻辑调用
    service = IssueService()
    status_code = service.create_issue(repo, issue_title, issue_body)

    if status_code == 204:
        logger.info("成功触发 Issue 创建！")
        logger.info(f"Issue 标题：{issue_title}")
    else:
        logger.error(f"触发失败，状态码：{status_code}")

if __name__ == "__main__":
    main()