# GitHub App + GitHub Action 自动化创建 Issue 项目
## 🎯 项目简介
本项目基于 **DDD（领域驱动设计）** 架构，实现了通过 **GitHub App 远程 API 触发 GitHub Action**，动态传参自动创建 GitHub Issue 的完整自动化流程。

核心能力：
- 仅支持外部 API 触发，禁止手动执行
- 动态传入 Issue 标题、内容，灵活自定义
- 严格遵循 GitHub 权限规范，安全可控
- 工程化 DDD 架构，可扩展、可维护、可直接用于生产/面试展示

---

## 📂 项目结构（DDD 四层架构）
```
Github-App-Trigger-Action/
├── .github/
│   └── workflows/
│       └── create-issue.yml          # GitHub Action 配置（仅API触发创建Issue）
├── src/
│   ├── __init__.py
│   ├── domain/                       # 领域层：核心业务模型
│   │   ├── __init__.py
│   │   └── github_app.py             # GitHub App 认证、JWT 生成
│   ├── application/                  # 应用层：业务流程编排
│   │   ├── __init__.py
│   │   └── issue_service.py          # 创建Issue的完整业务逻辑
│   ├── infrastructure/               # 基础设施层：外部API调用
│   │   ├── __init__.py
│   │   └── github_api_client.py      # GitHub API HTTP 客户端
│   └── interfaces/                   # 接口层：外部入口
│       ├── __init__.py
│       └── cli.py                    # 命令行启动入口
├── examples/
│   └── demo.py                       # 运行示例（已合并到cli.py）
├── .env                              # 本地环境变量（不上传GitHub）
├── .env.example                      # 环境变量模板（可上传）
├── .gitignore                        # 忽略敏感文件
├── requirements.txt                  # 项目依赖
└── README.md                         # 项目说明文档
```

---

## 🧱 架构分层说明
| 层级 | 职责 | 核心文件 |
|------|------|----------|
| **领域层（Domain）** | 封装核心业务逻辑，GitHub App 身份认证、JWT 生成 | `src/domain/github_app.py` |
| **应用层（Application）** | 编排业务流程，串联领域层与基础设施层，实现创建 Issue 全流程 | `src/application/issue_service.py` |
| **基础设施层（Infrastructure）** | 封装外部 API 调用，与 GitHub 服务交互 | `src/infrastructure/github_api_client.py` |
| **接口层（Interfaces）** | 提供外部调用入口，命令行启动脚本 | `src/interfaces/cli.py` |

---

## 🚀 快速开始
### 1. 前置条件
- 已创建 GitHub App，获取 `App ID`、`私钥文件（.pem）`、`Installation ID`
- 已给 GitHub App 配置 **Issues 读写权限**，并安装到目标仓库
- Python 3.10+ 环境

### 2. 环境配置
1.  克隆项目到本地
2.  复制 `.env.example` 为 `.env`，填写配置信息：
    ```env
    APP_ID=你的GitHub App ID
    INSTALLATION_ID=你的安装ID
    PRIVATE_KEY_PATH=private-key/app-key.pem
    REPO=Aiox123/Github-App-Trigger-Action  # 替换为你的仓库
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

### 3. 运行项目
```bash
python src/interfaces/cli.py
```
执行成功后，会自动触发 GitHub Action，在目标仓库创建 Issue。

---

## ⚙️ 核心配置说明
### 1. GitHub Action 配置（`create-issue.yml`）
```yaml
name: 外部 API 触发创建 Issue

on:
  repository_dispatch:
    types: [create-issue]

# 显式声明Issue写入权限，解决权限不足问题
permissions:
  issues: write

jobs:
  create-issue:
    runs-on: ubuntu-latest
    steps:
      - name: 创建 Issue
        uses: actions/github-script@v8  # 升级v8消除Node.js 20弃用警告
        with:
          script: |
            const { title, body } = context.payload.client_payload;
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: title,
              body: body
            });
```
- 仅支持 `repository_dispatch` 触发，严格遵循仅外部 API 调用要求
- 显式声明 `permissions: issues: write`，确保权限合规
- 升级 `actions/github-script@v8`，消除 Node.js 20 弃用警告

### 2. GitHub App 认证（`github_app.py`）
严格遵循 GitHub JWT 规范，有效期最大 10 分钟，避免认证失败：
```python
def generate_jwt(self):
    now = int(time.time())
    payload = {
        "iat": now - 30,      # 签发时间（提前30秒，避免时钟偏差）
        "exp": now + 600,     # 过期时间：最多10分钟（GitHub强制要求）
        "iss": self.app_id
    }
    return jwt.encode(payload, signing_key, algorithm="RS256")
```

---

## ✅ 验证成功标准
1.  **本地脚本执行**：返回 `✅ 成功触发 Issue 创建！`，无报错
2.  **GitHub Actions 页面**：`create-issue` 工作流状态为 **Success**
3.  **GitHub Issues 页面**：成功创建对应标题、内容的 Issue

---

## 📌 常见问题与解决方案
### 1. `ModuleNotFoundError: No module named 'src'`
- 解决方案：在 `cli.py` 顶部添加项目根目录到 Python 路径：
  ```python
  import sys
  from pathlib import Path
  sys.path.append(str(Path(__file__).parent.parent.parent))
  ```

### 2. `HttpError: Resource not accessible by integration`
- 解决方案：
  1.  给 GitHub App 配置 **Issues 读写权限**
  2.  Action 中显式声明 `permissions: issues: write`
  3.  重新安装 GitHub App 到仓库，刷新权限

### 3. `'Expiration time' claim ('exp') is too far in the future`
- 解决方案：严格控制 JWT 有效期，`exp` 不超过 600 秒（10 分钟）

### 4. `KeyError: 'token'`
- 解决方案：检查 `APP_ID`、`INSTALLATION_ID`、私钥路径是否正确，确保 JWT 生成合规

---

## 📦 依赖清单
```txt
pyjwt==2.8.0
python-dotenv==1.0.1
requests==2.31.0
cryptography==41.0.7
```

---

## 🎯 项目亮点
1.  **标准 DDD 架构**：职责清晰，分层明确，符合工程化开发规范
2.  **安全可控**：敏感文件不上传 GitHub，权限严格管控
3.  **灵活可扩展**：可快速对接 Jira、企业微信等系统，实现更多自动化场景
4.  **无冗余代码**：极简实现，仅保留核心功能，易于维护
5.  **面试友好**：完整的 GitHub App + GitHub Action 实战项目，可直接用于技术面试展示

---

## 📄 许可证
MIT License

---

## 🤝 贡献
欢迎提交 Issue 和 PR，一起完善项目！

---

## ✨ 最终状态
本项目已完成全链路验证，所有功能正常运行，可直接用于生产环境或技术展示。

---
