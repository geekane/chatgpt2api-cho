#!/bin/bash

# Choreo 部署脚本
# 使用 Choreo CLI 将 ChatGPT2API 部署到 Choreo 平台

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== ChatGPT2API Choreo 部署脚本 ===${NC}"

# 检查 Choreo CLI 是否安装
if ! command -v wdp &> /dev/null; then
    echo -e "${RED}错误: Choreo CLI (wdp) 未安装${NC}"
    echo "请运行以下命令安装:"
    echo "curl -o- https://raw.githubusercontent.com/wso2/wdp-cli/main/scripts/install.sh | bash"
    exit 1
fi

echo -e "${GREEN}✓ Choreo CLI 已安装${NC}"

# 配置变量
PROJECT_NAME="${PROJECT_NAME:-chatgpt2api}"
BACKEND_COMPONENT="chatgpt2api-backend"
FRONTEND_COMPONENT="chatgpt2api-frontend"
ENVIRONMENT="${ENVIRONMENT:-development}"

# 登录 Choreo
echo -e "${YELLOW}步骤 1: 登录 Choreo 平台${NC}"
wdp login

# 创建项目（如果不存在）
echo -e "${YELLOW}步骤 2: 创建项目${NC}"
if wdp get project "$PROJECT_NAME" &> /dev/null; then
    echo -e "${GREEN}✓ 项目 '$PROJECT_NAME' 已存在${NC}"
else
    echo "创建新项目: $PROJECT_NAME"
    wdp create project "$PROJECT_NAME" --type=multi-repository
    echo -e "${GREEN}✓ 项目创建成功${NC}"
fi

# 创建后端组件
echo -e "${YELLOW}步骤 3: 创建后端服务组件${NC}"
if wdp get component "$BACKEND_COMPONENT" --project="$PROJECT_NAME" &> /dev/null; then
    echo -e "${GREEN}✓ 后端组件已存在${NC}"
else
    echo "创建后端组件: $BACKEND_COMPONENT"
    wdp create component "$BACKEND_COMPONENT" \
        --project="$PROJECT_NAME" \
        --type=service \
        --language=python \
        --buildpack=python
    echo -e "${GREEN}✓ 后端组件创建成功${NC}"
fi

# 创建前端组件
echo -e "${YELLOW}步骤 4: 创建前端 Web 应用组件${NC}"
if wdp get component "$FRONTEND_COMPONENT" --project="$PROJECT_NAME" &> /dev/null; then
    echo -e "${GREEN}✓ 前端组件已存在${NC}"
else
    echo "创建前端组件: $FRONTEND_COMPONENT"
    wdp create component "$FRONTEND_COMPONENT" \
        --project="$PROJECT_NAME" \
        --type=web-application \
        --language=nodejs \
        --buildpack=nodejs
    echo -e "${GREEN}✓ 前端组件创建成功${NC}"
fi

# 设置环境变量
echo -e "${YELLOW}步骤 5: 配置环境变量${NC}"
read -p "请输入 CHATGPT2API_AUTH_KEY (默认: chatgpt2api): " AUTH_KEY
AUTH_KEY=${AUTH_KEY:-chatgpt2api}

wdp set env "$BACKEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --env="$ENVIRONMENT" \
    --key=CHATGPT2API_AUTH_KEY \
    --value="$AUTH_KEY"

echo -e "${GREEN}✓ 环境变量配置完成${NC}"

# 触发后端构建
echo -e "${YELLOW}步骤 6: 触发后端构建${NC}"
BACKEND_BUILD_ID=$(wdp create build "$BACKEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --output=json | jq -r '.id')

echo "后端构建 ID: $BACKEND_BUILD_ID"
echo "等待构建完成..."

# 等待构建完成
while true; do
    BUILD_STATUS=$(wdp get build "$BACKEND_BUILD_ID" \
        --component="$BACKEND_COMPONENT" \
        --project="$PROJECT_NAME" \
        --output=json | jq -r '.status')
    
    if [ "$BUILD_STATUS" == "SUCCESS" ]; then
        echo -e "${GREEN}✓ 后端构建成功${NC}"
        break
    elif [ "$BUILD_STATUS" == "FAILED" ]; then
        echo -e "${RED}✗ 后端构建失败${NC}"
        exit 1
    else
        echo "构建状态: $BUILD_STATUS"
        sleep 10
    fi
done

# 部署后端
echo -e "${YELLOW}步骤 7: 部署后端服务${NC}"
wdp create deployment "$BACKEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --env="$ENVIRONMENT" \
    --build-id="$BACKEND_BUILD_ID"

echo -e "${GREEN}✓ 后端部署完成${NC}"

# 获取后端 URL
BACKEND_URL=$(wdp get component "$BACKEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --output=json | jq -r ".environments[] | select(.name==\"$ENVIRONMENT\") | .url")

echo "后端 URL: $BACKEND_URL"

# 设置前端环境变量
wdp set env "$FRONTEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --env="$ENVIRONMENT" \
    --key=NEXT_PUBLIC_API_URL \
    --value="$BACKEND_URL"

# 触发前端构建
echo -e "${YELLOW}步骤 8: 触发前端构建${NC}"
FRONTEND_BUILD_ID=$(wdp create build "$FRONTEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --output=json | jq -r '.id')

echo "前端构建 ID: $FRONTEND_BUILD_ID"
echo "等待构建完成..."

# 等待构建完成
while true; do
    BUILD_STATUS=$(wdp get build "$FRONTEND_BUILD_ID" \
        --component="$FRONTEND_COMPONENT" \
        --project="$PROJECT_NAME" \
        --output=json | jq -r '.status')
    
    if [ "$BUILD_STATUS" == "SUCCESS" ]; then
        echo -e "${GREEN}✓ 前端构建成功${NC}"
        break
    elif [ "$BUILD_STATUS" == "FAILED" ]; then
        echo -e "${RED}✗ 前端构建失败${NC}"
        exit 1
    else
        echo "构建状态: $BUILD_STATUS"
        sleep 10
    fi
done

# 部署前端
echo -e "${YELLOW}步骤 9: 部署前端应用${NC}"
wdp create deployment "$FRONTEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --env="$ENVIRONMENT" \
    --build-id="$FRONTEND_BUILD_ID"

echo -e "${GREEN}✓ 前端部署完成${NC}"

# 获取前端 URL
FRONTEND_URL=$(wdp get component "$FRONTEND_COMPONENT" \
    --project="$PROJECT_NAME" \
    --output=json | jq -r ".environments[] | select(.name==\"$ENVIRONMENT\") | .url")

echo ""
echo -e "${GREEN}=== 部署完成 ===${NC}"
echo "后端 API: $BACKEND_URL"
echo "前端应用: $FRONTEND_URL"
echo ""
echo "查看日志:"
echo "  后端: wdp logs application --component $BACKEND_COMPONENT --project $PROJECT_NAME --env $ENVIRONMENT --follow"
echo "  前端: wdp logs application --component $FRONTEND_COMPONENT --project $PROJECT_NAME --env $ENVIRONMENT --follow"
