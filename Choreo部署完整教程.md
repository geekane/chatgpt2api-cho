# 🚀 ChatGPT2API 部署到 Choreo 完整教程

## 📌 你的项目信息
- **GitHub 仓库**: https://github.com/geekane/chatgpt2api-cho.git
- **分支**: master
- **默认密钥**: chatgpt2api

---

## 第一步：推送最新代码到 GitHub

### 1.1 添加新创建的部署文件

打开命令行（PowerShell 或 CMD），进入项目目录：

```powershell
cd d:\chatgpt2api
```

### 1.2 添加并提交文件

```powershell
git add .
git commit -m "Add Choreo deployment configuration"
git push origin master
```

**说明**：这会将所有新创建的 Choreo 配置文件推送到 GitHub。

---

## 第二步：注册并登录 Choreo

### 2.1 访问 Choreo 控制台

在浏览器中打开：
```
https://console.choreo.dev/
```

### 2.2 注册/登录

- 如果没有账号，点击 **Sign Up** 注册
- 可以使用 Google、GitHub 或邮箱注册
- 如果已有账号，直接 **Sign In** 登录

### 2.3 创建组织（首次使用）

- 登录后会提示创建组织（Organization）
- 输入组织名称，例如：`my-org`
- 点击 **Create**

---

## 第三步：创建项目

### 3.1 创建新项目

1. 在 Choreo 控制台首页，点击 **Create** 按钮
2. 选择 **Project**
3. 填写项目信息：
   - **Project Name**: `chatgpt2api`
   - **Description**: `ChatGPT to API converter`（可选）
4. 点击 **Create**

---

## 第四步：创建后端服务组件

### 4.1 创建 Service 组件

1. 在项目页面，点击 **Create** → **Service**
2. 填写组件信息：
   - **Component Name**: `chatgpt2api-backend`
   - **Description**: `Backend API service`（可选）

### 4.2 连接 GitHub 仓库

1. 在 **Connect Repository** 页面：
   - 选择 **GitHub**
   - 点击 **Authorize** 授权 Choreo 访问你的 GitHub
   - 授权完成后，选择你的仓库：`geekane/chatgpt2api-cho`
   - **Branch**: `master`
   - 点击 **Next**

### 4.3 配置构建设置

1. **Buildpack Type**: 选择 **Dockerfile**
2. **Dockerfile Path**: 输入 `./Dockerfile`
3. **Docker Context Path**: 输入 `.`（当前目录）
4. **Port**: 输入 `80`（Dockerfile 中暴露的端口）
5. 点击 **Create**

---

## 第五步：配置环境变量

### 5.1 进入组件设置

1. 组件创建后，点击左侧菜单的 **Configs & Secrets**
2. 选择 **Environment Variables** 标签

### 5.2 添加环境变量

点击 **Add** 按钮，添加以下环境变量：

#### 必需的环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `CHATGPT2API_AUTH_KEY` | `chatgpt2api` | API 认证密钥（可自定义） |
| `STORAGE_BACKEND` | `json` | 存储方式 |
| `PYTHONUNBUFFERED` | `1` | Python 输出不缓冲 |

#### 可选的环境变量（根据需要添加）：

| 变量名 | 值示例 | 说明 |
|--------|--------|------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | 使用 PostgreSQL 时 |
| `GIT_REPO_URL` | `https://github.com/user/repo.git` | 使用 Git 存储时 |
| `GIT_TOKEN` | `ghp_xxxxx` | Git 访问令牌 |

### 5.3 保存配置

添加完所有环境变量后，点击 **Save**。

---

## 第六步：构建应用

### 6.1 触发构建

1. 点击左侧菜单的 **Build**
2. 点击右上角的 **Build** 按钮
3. 确认构建配置，点击 **Build**

### 6.2 等待构建完成

- 构建过程可能需要 **5-10 分钟**
- 你可以点击构建记录查看实时日志
- 构建状态会显示：
  - 🔵 **Building** - 构建中
  - 🟢 **Success** - 构建成功
  - 🔴 **Failed** - 构建失败

### 6.3 如果构建失败

1. 点击失败的构建记录
2. 查看 **Build Logs**
3. 根据错误信息调整代码或配置
4. 重新触发构建

---

## 第七步：部署到 Development 环境

### 7.1 部署应用

1. 构建成功后，点击左侧菜单的 **Deploy**
2. 选择 **Development** 环境
3. 选择刚才成功的构建版本
4. 点击 **Deploy** 按钮
5. 确认部署，点击 **Deploy**

### 7.2 等待部署完成

- 部署过程通常需要 **2-5 分钟**
- 部署状态：
  - 🔵 **Deploying** - 部署中
  - 🟢 **Active** - 部署成功，服务运行中
  - 🔴 **Failed** - 部署失败

---

## 第八步：获取访问 URL

### 8.1 查看服务 URL

1. 部署成功后，在 **Deploy** 页面可以看到服务 URL
2. URL 格式类似：`https://chatgpt2api-backend-xxxxx.choreoapis.dev`
3. 复制这个 URL

### 8.2 测试 API

打开浏览器或使用 curl 测试：

```bash
# 测试模型列表接口
curl https://your-backend-url/v1/models \
  -H "Authorization: Bearer chatgpt2api"
```

**预期响应**：返回可用的模型列表（JSON 格式）

---

## 第九步：添加 ChatGPT 账号

### 9.1 使用 API 添加账号

```powershell
# Windows PowerShell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer chatgpt2api"
}
$body = @{
    tokens = @("你的access_token")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-backend-url/api/accounts" -Method Post -Headers $headers -Body $body
```

### 9.2 获取 access_token 的方法

1. 登录 ChatGPT 官网：https://chatgpt.com
2. 打开浏览器开发者工具（F12）
3. 切换到 **Application** 或 **存储** 标签
4. 找到 **Cookies** → `https://chatgpt.com`
5. 复制 `__Secure-next-auth.session-token` 的值

或者：

1. 在 ChatGPT 页面打开开发者工具（F12）
2. 切换到 **Network** 标签
3. 刷新页面
4. 找到任意请求，查看请求头中的 `Authorization: Bearer eyJhbGci...`
5. 复制 `Bearer` 后面的 token

---

## 第十步：（可选）部署前端应用

### 10.1 创建前端组件

1. 回到项目页面，点击 **Create** → **Web Application**
2. 填写信息：
   - **Component Name**: `chatgpt2api-frontend`
   - **Description**: `Frontend web interface`

### 10.2 连接仓库

- 选择相同的 GitHub 仓库：`geekane/chatgpt2api-cho`
- **Branch**: `master`

### 10.3 配置构建

1. **Buildpack Type**: 选择 **Dockerfile** 或 **Node.js**
2. 如果选择 Node.js：
   - **Build Command**: `cd web && npm install && npm run build`
   - **Start Command**: `cd web && npm start`
   - **Port**: `3000`
3. 如果选择 Dockerfile：
   - 使用项目根目录的 Dockerfile（已包含前端构建）

### 10.4 配置环境变量

添加环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend-url` | 后端 API 地址 |
| `NODE_ENV` | `production` | 生产环境 |

### 10.5 构建和部署

- 触发构建
- 等待构建完成
- 部署到 Development 环境
- 获取前端 URL

---

## 📊 部署后的管理

### 查看日志

1. 在组件页面，点击 **Observability** → **Logs**
2. 选择环境（Development）
3. 查看实时日志

### 监控性能

1. 点击 **Observability** → **Metrics**
2. 查看 CPU、内存、请求数等指标

### 更新部署

1. 修改代码后推送到 GitHub
2. 在 Choreo 中触发新的构建
3. 部署新版本

---

## 🔧 常见问题

### 1. 构建失败：找不到 Dockerfile

**解决方案**：
- 确保 Dockerfile 在项目根目录
- 检查 Dockerfile 路径配置是否正确：`./Dockerfile`

### 2. 部署失败：端口错误

**解决方案**：
- 确保配置的端口与 Dockerfile 中 EXPOSE 的端口一致
- 本项目使用端口 `80`

### 3. API 返回 401 Unauthorized

**解决方案**：
- 检查请求头中的 `Authorization: Bearer chatgpt2api`
- 确认环境变量 `CHATGPT2API_AUTH_KEY` 设置正确

### 4. 无法添加账号

**解决方案**：
- 确认 access_token 格式正确
- 检查后端日志查看错误信息
- 确保存储后端配置正确

### 5. 构建时间过长

**解决方案**：
- 这是正常的，首次构建需要下载所有依赖
- 后续构建会使用缓存，速度会快很多

---

## 🎉 完成！

部署完成后，你将拥有：

- ✅ **后端 API**：`https://chatgpt2api-backend-xxxxx.choreoapis.dev`
- ✅ **前端界面**（如果部署）：`https://chatgpt2api-frontend-xxxxx.choreoapis.dev`

### 使用 API

```bash
# 文生图
curl https://your-backend-url/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer chatgpt2api" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "一只可爱的猫",
    "n": 1
  }'
```

### 接入第三方客户端

- **API 地址**：`https://your-backend-url/v1`
- **API Key**：`chatgpt2api`
- **支持的模型**：gpt-image-2, codex-gpt-image-2, auto, gpt-5 等

---

## 📞 需要帮助？

- 查看 Choreo 官方文档：https://wso2.com/choreo/docs/
- 查看项目 README：`README.md`
- 查看完整部署文档：`CHOREO_DEPLOYMENT.md`

---

**祝你部署顺利！** 🚀
