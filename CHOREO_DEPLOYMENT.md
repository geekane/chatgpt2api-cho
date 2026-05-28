# ChatGPT2API Choreo 部署指南

本指南介绍如何将 ChatGPT2API 项目部署到 WSO2 Choreo 平台。

## 📋 前置要求

### 1. Choreo 账号
- 注册 Choreo 账号：https://console.choreo.dev/
- 创建组织（如果还没有）

### 2. 安装 Choreo CLI

**Linux/macOS:**
```bash
curl -o- https://raw.githubusercontent.com/wso2/wdp-cli/main/scripts/install.sh | bash
```

**验证安装:**
```bash
wdp --version
```

## 🚀 部署方式

### 方式 1：使用 Python 脚本部署（推荐）

这是最简单的部署方式，适用于 Windows、Linux 和 macOS。

```bash
# 确保已安装 Python 3.7+
python deploy-to-choreo.py
```

脚本会自动：
1. 检查 Choreo CLI 是否安装
2. 登录 Choreo 平台
3. 创建项目和组件
4. 配置环境变量
5. 构建和部署后端服务
6. 构建和部署前端应用
7. 输出访问 URL

### 方式 2：使用 Bash 脚本部署

适用于 Linux 和 macOS（需要安装 `jq`）。

```bash
chmod +x deploy-to-choreo.sh
./deploy-to-choreo.sh
```

### 方式 3：手动部署

#### 步骤 1：登录 Choreo
```bash
wdp login
```

#### 步骤 2：创建项目
```bash
wdp create project chatgpt2api --type=multi-repository
```

#### 步骤 3：创建后端组件
```bash
wdp create component chatgpt2api-backend \
  --project=chatgpt2api \
  --type=service \
  --language=python \
  --buildpack=python
```

#### 步骤 4：创建前端组件
```bash
wdp create component chatgpt2api-frontend \
  --project=chatgpt2api \
  --type=web-application \
  --language=nodejs \
  --buildpack=nodejs
```

#### 步骤 5：设置后端环境变量
```bash
wdp set env chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --key=CHATGPT2API_AUTH_KEY \
  --value=your_secret_key
```

#### 步骤 6：构建后端
```bash
wdp create build chatgpt2api-backend --project=chatgpt2api
```

获取构建 ID 后，等待构建完成。

#### 步骤 7：部署后端
```bash
wdp create deployment chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --build-id=<BUILD_ID>
```

#### 步骤 8：获取后端 URL 并配置前端
```bash
# 获取后端 URL
wdp get component chatgpt2api-backend --project=chatgpt2api

# 设置前端环境变量
wdp set env chatgpt2api-frontend \
  --project=chatgpt2api \
  --env=development \
  --key=NEXT_PUBLIC_API_URL \
  --value=<BACKEND_URL>
```

#### 步骤 9：构建和部署前端
```bash
# 构建
wdp create build chatgpt2api-frontend --project=chatgpt2api

# 部署
wdp create deployment chatgpt2api-frontend \
  --project=chatgpt2api \
  --env=development \
  --build-id=<BUILD_ID>
```

### 方式 4：使用 GitHub Actions 自动部署

#### 步骤 1：配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

- `CHOREO_TOKEN`: Choreo 平台的访问令牌
- `CHATGPT2API_AUTH_KEY`: API 认证密钥（默认：chatgpt2api）

#### 步骤 2：触发部署

**自动触发：** 推送代码到 `main` 分支

```bash
git push origin main
```

**手动触发：** 在 GitHub Actions 页面手动运行工作流

## 📊 监控和日志

### 查看后端日志
```bash
wdp logs application \
  --component chatgpt2api-backend \
  --project chatgpt2api \
  --env development \
  --follow
```

### 查看前端日志
```bash
wdp logs application \
  --component chatgpt2api-frontend \
  --project chatgpt2api \
  --env development \
  --follow
```

### 查看构建日志
```bash
wdp logs build \
  --component chatgpt2api-backend \
  --project chatgpt2api \
  --build-id <BUILD_ID>
```

## 🔧 配置说明

### 环境变量

**后端环境变量：**
- `CHATGPT2API_AUTH_KEY`: API 认证密钥（必需）
- `STORAGE_BACKEND`: 存储后端类型（json/sqlite/postgres/git）
- `DATABASE_URL`: 数据库连接字符串（使用 postgres 时）
- `GIT_REPO_URL`: Git 仓库地址（使用 git 存储时）
- `GIT_TOKEN`: Git 访问令牌（使用 git 存储时）

**前端环境变量：**
- `NEXT_PUBLIC_API_URL`: 后端 API 地址
- `NODE_ENV`: 运行环境（production）

### 存储配置

Choreo 部署推荐使用以下存储方式：

1. **PostgreSQL（推荐）**
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

2. **Git 私有仓库**
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

## 🔄 更新部署

### 更新后端
```bash
# 触发新构建
wdp create build chatgpt2api-backend --project=chatgpt2api

# 部署新版本
wdp create deployment chatgpt2api-backend \
  --project=chatgpt2api \
  --env=development \
  --build-id=<NEW_BUILD_ID>
```

### 更新前端
```bash
# 触发新构建
wdp create build chatgpt2api-frontend --project=chatgpt2api

# 部署新版本
wdp create deployment chatgpt2api-frontend \
  --project=chatgpt2api \
  --env=development \
  --build-id=<NEW_BUILD_ID>
```

## 🐛 故障排查

### 构建失败

1. 查看构建日志：
   ```bash
   wdp logs build --component <COMPONENT> --project chatgpt2api --build-id <BUILD_ID>
   ```

2. 常见问题：
   - Python 依赖安装失败：检查 `requirements.txt`
   - Node.js 构建失败：检查 `package.json` 和构建命令
   - 内存不足：增加组件资源配置

### 部署失败

1. 查看应用日志：
   ```bash
   wdp logs application --component <COMPONENT> --project chatgpt2api --env development
   ```

2. 常见问题：
   - 端口配置错误：确保后端使用 8001，前端使用 3000
   - 环境变量缺失：检查所有必需的环境变量
   - 健康检查失败：确保健康检查路径正确

### 连接问题

1. 前端无法连接后端：
   - 检查 `NEXT_PUBLIC_API_URL` 是否正确设置
   - 确认后端服务已成功部署
   - 检查 CORS 配置

2. 数据库连接失败：
   - 验证 `DATABASE_URL` 格式
   - 确认数据库可从 Choreo 访问
   - 检查数据库凭据

## 📚 更多资源

- [Choreo 官方文档](https://wso2.com/choreo/docs/)
- [Choreo CLI 文档](https://wso2.com/choreo/docs/develop-components/develop-services/develop-a-service/#use-the-choreo-cli)
- [ChatGPT2API 项目文档](./README.md)

## 💡 提示

1. **生产环境部署**：将 `--env=development` 改为 `--env=production`
2. **多环境管理**：为不同环境创建不同的配置
3. **自动化部署**：使用 GitHub Actions 实现 CI/CD
4. **监控告警**：配置 Choreo 的监控和告警功能
5. **备份策略**：定期备份账号数据和配置

## ⚠️ 注意事项

1. **安全性**：
   - 不要在代码中硬编码敏感信息
   - 使用环境变量管理密钥
   - 定期更新 `CHATGPT2API_AUTH_KEY`

2. **资源限制**：
   - 注意 Choreo 平台的资源配额
   - 根据需要调整组件资源配置

3. **成本控制**：
   - 了解 Choreo 的定价模型
   - 监控资源使用情况

4. **合规性**：
   - 遵守 OpenAI 服务条款
   - 仅用于个人学习和研究
