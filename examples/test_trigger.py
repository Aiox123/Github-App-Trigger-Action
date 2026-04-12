import sys
from pathlib import Path

# 动态获取项目根目录（rovo 文件夹），并添加到 sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 原导入语句
from src.action_trigger import ActionController

if __name__ == "__main__":
    print("🔹 开始测试 GitHub App 触发 Action")
    controller = ActionController()
    
    if controller.trigger_action():
        print("✅ Action 触发成功！")
    else:
        print("❌ 触发失败")