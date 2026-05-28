# Choreo 部署配置说明

## 📋 配置文件

### component.yaml
Choreo 组件配置文件，定义了服务的构建和运行方式。

## 🔧 当前配置

### 后端服务 (chatgpt2api-backend)

- **类型**: Service
- **构建方式**: Dockerfile
- **端口**: 8080
- **健康检查**: GET /v1/models
- **用户**: 非 root 用户 (UID: 10001)

#### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `CHATGPT2API_AUTH_KEY` | `${CHATGPT2API_AUTH_KEY}` | API 认证密钥（需在 Choreo 中配置） |
| `STORAGE_BACKEND` | `json` | 存储后端类型 |
| `PYTHONUNBUFFERED` | `1` | Python 输出不缓冲 |

#### 资源配置

- **请求**: 512Mi 内存, 500m CPU
- **限制**: 1Gi 内存, 1000m CPU

## 🚀 部署步骤

### 1. 在 Choreo 控制台创建组件

1. 访问 https://console.choreo.dev/
2. 创建项目（如果还没有）
3. 创建 Service 组件
4. 连接 GitHub 仓库
5. 选择分支：`master`

### 2. 配置构建

- **Buildpack**: 选择 **Dockerfile**
- **Dockerfile Path**: `./Dockerfile`
- **Docker Context**: `.`
- **Port**: `8080`

### 3. 配置环境变量

在 Choreo 控制台的 **Configs & Secrets** 中添加：

```
CHATGPT2API_AUTH_KEY=chatgpt2api
```

可选的环境变量（根据需要添加）：

```
# 使用 PostgreSQL
STORAGE_BACKEND=postgres
DATABASE_URL=postgresql://user:password@host:5432/dbname

# 使用 Git 存储
STORAGE_BACKEND=git
GIT_REPO_URL=https://github.com/user/repo.git
GIT_TOKEN=your_token
```

### 4. 构建和部署

1. 触发构建（Build）
2. 等待构建完成（约 5-10 分钟）
3. 部署到 Development 环境
4. 获取服务 URL

### 5. 测试 API

```bash
curl https://your-service-url/v1/models \
  -H "Authorization: Bearer chatgpt2api"
```

## 🔒 安全配置

### 非 root 用户

Dockerfile 已配置为使用非 root 用户运行：

```dockerfile
RUN useradd -u 10001 -m choreouser && \
    chown -R 10001:10001 /app
USER 10001
```

这符合 Choreo 的安全最佳实践。

### 端口配置

使用端口 **8080** 而不是特权端口（< 1024），避免需要 root 权限。

## 📊 架构说明

### 单容器部署

当前配置使用单个 Docker 容器同时提供：
- 后端 API 服务（FastAPI）
- 前端静态文件（Next.js 构建输出）

这种方式的优点：
- ✅ 部署简单，只需一个组件
- ✅ 资源占用少
- ✅ 无需配置跨域（CORS）
- ✅ 统一的访问 URL

### 前端访问

前端静态文件已集成在 Docker 镜像中（`/app/web_dist`），可以通过后端服务访问。

如果需要单独部署前端，可以：
1. 取消 `component.yaml` 中前端配置的注释
2. 创建独立的前端组件
3. 配置 `NEXT_PUBLIC_API_URL` 指向后端服务

## 🔄 更新部署

### 代码更新

1. 推送代码到 GitHub
2. 在 Choreo 中触发新构建
3. 部署新版本

### 配置更新

1. 在 Choreo 控制台修改环境变量
2. 重新部署（无需重新构建）

## 📝 注意事项

1. **首次构建时间较长**：需要下载所有依赖，约 5-10 分钟
2. **后续构建会更快**：利用 Docker 层缓存
3. **环境变量敏感信息**：不要在 component.yaml 中硬编码，使用 Choreo 的 Secrets 管理
4. **资源限制**：根据实际使用情况调整内存和 CPU 配置
5. **健康检查**：确保 `/v1/models` 端点可访问且不需要认证

## 🆘 故障排查

### 构建失败

1. 查看构建日志
2. 检查 Dockerfile 语法
3. 确认所有依赖文件存在

### 部署失败

1. 查看应用日志
2. 检查端口配置（8080）
3. 验证环境变量设置
4. 确认健康检查端点可访问

### 服务无响应

1. 检查健康检查状态
2. 查看应用日志
3. 验证端口映射正确
4. 确认防火墙规则

## 📚 相关文档

- [Choreo 官方文档](https://wso2.com/choreo/docs/)
- [项目 README](../README.md)
- [完整部署教程](../Choreo部署完整教程.md)
