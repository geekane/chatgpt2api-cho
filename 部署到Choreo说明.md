# 🚀 ChatGPT2API 部署到 Choreo 平台

## 📦 已创建的文件

我已经为你创建了完整的 Choreo 部署配置和脚本：

### 1. 配置文件
- `.choreo/component.yaml` - Choreo 组件配置
- `requirements.txt` - Python 依赖列表

### 2. 部署脚本
- `deploy-to-choreo.py` - **Python 部署脚本（推荐使用）**
- `deploy-to-choreo.sh` - Bash 部署脚本（Linux/macOS）
- `choreo-quickstart.bat` - Windows 快速启动脚本

### 3. CI/CD 配置
- `.github/workflows/choreo-deploy.yml` - GitHub Actions 自动部署工作流

### 4. 文档
- `CHOREO_DEPLOYMENT.md` - 完整的部署指南

## 🎯 快速开始

### Windows 用户（最简单）

1. **双击运行：**
   ```
   choreo-quickstart.bat
   ```

2. **或使用命令行：**
   ```cmd
   python deploy-to-choreo.py
   ```

### Linux/macOS 用户

```bash
# 方式 1：使用 Python 脚本
python3 deploy-to-choreo.py

# 方式 2：使用 Bash 脚本
chmod +x deploy-to-choreo.sh
./deploy-to-choreo.sh
```

## 📋 部署前准备

### 1. 安装 Choreo CLI

**Linux/macOS:**
```bash
curl -o- https://raw.githubusercontent.com/wso2/wdp-cli/main/scripts/install.sh | bash
```

**验证安装:**
```bash
wdp --version
```

### 2. 注册 Choreo 账号

访问：https://console.choreo.dev/

### 3. 准备配置信息

- **API 密钥**：默认是 `chatgpt2api`，可以自定义
- **存储方式**：建议使用 PostgreSQL 或 Git 私有仓库

## 🔄 部署流程

运行部署脚本后，会自动执行以下步骤：

1. ✅ 检查 Choreo CLI 是否安装
2. ✅ 登录 Choreo 平台
3. ✅ 创建项目 `chatgpt2api`
4. ✅ 创建后端服务组件
5. ✅ 创建前端 Web 应用组件
6. ✅ 配置环境变量
7. ✅ 构建后端服务
8. ✅ 部署后端服务
9. ✅ 构建前端应用
10. ✅ 部署前端应用
11. ✅ 输出访问 URL

## 📊 部署后操作

### 查看日志

**后端日志：**
```bash
wdp logs application --component chatgpt2api-backend --project chatgpt2api --env development --follow
```

**前端日志：**
```bash
wdp logs application --component chatgpt2api-frontend --project chatgpt2api --env development --follow
```

### 添加账号

部署完成后，访问前端 URL，在账号管理页面添加你的 ChatGPT access_token。

### 使用 API

```bash
# 获取模型列表
curl https://your-backend-url/v1/models \
  -H "Authorization: Bearer chatgpt2api"

# 生成图片
curl https://your-backend-url/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer chatgpt2api" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "一只可爱的猫",
    "n": 1
  }'
```

## 🔧 高级配置

### 使用 PostgreSQL 存储

```bash
wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=STORAGE_BACKEND \
  --value=postgres

wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=DATABASE_URL \
  --value=postgresql://user:password@host:5432/dbname
```

### 使用 Git 私有仓库存储

```bash
wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=STORAGE_BACKEND \
  --value=git

wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=GIT_REPO_URL \
  --value=https://github.com/your-username/your-private-repo.git

wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=GIT_TOKEN \
  --value=your_git_token
```

## 🤖 使用 GitHub Actions 自动部署

### 1. 配置 GitHub Secrets

在你的 GitHub 仓库设置中添加：

- `CHOREO_TOKEN` - Choreo 平台访问令牌
- `CHATGPT2API_AUTH_KEY` - API 认证密钥

### 2. 推送代码触发部署

```bash
git add .
git commit -m "Deploy to Choreo"
git push origin main
```

GitHub Actions 会自动构建和部署到 Choreo。

## 📚 相关文档

- **完整部署指南**：查看 `CHOREO_DEPLOYMENT.md`
- **项目文档**：查看 `README.md`
- **Choreo 官方文档**：https://wso2.com/choreo/docs/

## ⚠️ 重要提示

1. **默认密钥**：`chatgpt2api`（建议修改）
2. **端口配置**：
   - 后端：8001
   - 前端：3000
3. **存储方式**：默认使用 JSON 文件，生产环境建议使用 PostgreSQL
4. **安全性**：不要在代码中硬编码敏感信息，使用环境变量

## 🆘 需要帮助？

如果遇到问题：

1. 查看 `CHOREO_DEPLOYMENT.md` 中的故障排查部分
2. 检查 Choreo CLI 日志
3. 查看组件构建和部署日志
4. 访问 Choreo 官方文档

## ✨ 下一步

1. 运行部署脚本
2. 等待构建和部署完成
3. 访问前端 URL
4. 添加 ChatGPT 账号
5. 开始使用 API！

---

**祝部署顺利！** 🎉
