#!/usr/bin/env python3
"""
ChatGPT2API Choreo 部署脚本 (使用 REST API)
适用于 Windows 系统，不需要安装 Choreo CLI
"""

import requests
import json
import time
import sys
import os
from typing import Optional, Dict, Any

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(message: str, color: str):
    """彩色输出"""
    if os.name == 'nt':  # Windows
        print(message)
    else:
        print(f"{color}{message}{Colors.NC}")

def print_step(step: int, message: str):
    """打印步骤"""
    print_color(f"\n{'='*60}", Colors.BLUE)
    print_color(f"步骤 {step}: {message}", Colors.YELLOW)
    print_color(f"{'='*60}", Colors.BLUE)

def print_success(message: str):
    """打印成功消息"""
    print_color(f"✓ {message}", Colors.GREEN)

def print_error(message: str):
    """打印错误消息"""
    print_color(f"✗ {message}", Colors.RED)

def print_info(message: str):
    """打印信息"""
    print(f"  {message}")

class ChoreoDeployer:
    """Choreo 部署器"""
    
    def __init__(self):
        self.base_url = "https://api.choreo.dev/api/v1"
        self.console_url = "https://console.choreo.dev"
        self.access_token = None
        self.org_id = None
        self.project_id = None
        
    def get_auth_instructions(self):
        """获取认证说明"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("Choreo 平台认证", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        print("由于 Choreo CLI 在 Windows 上不可用，我们需要使用 Web 控制台部署。")
        print()
        print_color("请按照以下步骤操作：", Colors.YELLOW)
        print()
        print("1. 访问 Choreo 控制台：")
        print_color(f"   {self.console_url}", Colors.BLUE)
        print()
        print("2. 登录你的账号（如果还没有账号，请先注册）")
        print()
        print("3. 创建新项目或选择现有项目")
        print()
        print("4. 我们将使用 Docker 部署方式（推荐）")
        print()
        
    def show_docker_deployment_guide(self):
        """显示 Docker 部署指南"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("Docker 部署指南", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        print_color("方案 1: 使用现有的 Dockerfile（推荐）", Colors.GREEN)
        print()
        print("项目已包含 Dockerfile，可以直接部署到 Choreo。")
        print()
        print_color("步骤：", Colors.YELLOW)
        print("1. 将代码推送到 GitHub 仓库")
        print("2. 在 Choreo 控制台创建新组件")
        print("3. 选择 'Service' 类型")
        print("4. 连接你的 GitHub 仓库")
        print("5. Choreo 会自动检测 Dockerfile 并构建")
        print()
        
        print_color("方案 2: 使用 Choreo GitHub Action", Colors.GREEN)
        print()
        print("项目已包含 GitHub Actions 工作流配置。")
        print()
        print_color("步骤：", Colors.YELLOW)
        print("1. 在 GitHub 仓库设置中添加 Secrets：")
        print("   - CHOREO_TOKEN: Choreo 访问令牌")
        print("   - CHATGPT2API_AUTH_KEY: API 密钥")
        print()
        print("2. 推送代码到 main 分支，自动触发部署")
        print()
        
        print_color("方案 3: 手动部署（Web 控制台）", Colors.GREEN)
        print()
        print("使用 Choreo Web 控制台手动创建和部署组件。")
        print()
        
    def show_manual_deployment_steps(self):
        """显示手动部署步骤"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("手动部署详细步骤", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        print_color("第一步：准备 GitHub 仓库", Colors.YELLOW)
        print("1. 将项目代码推送到 GitHub（公开或私有仓库）")
        print("2. 确保仓库包含 Dockerfile 和所有必要文件")
        print()
        
        print_color("第二步：在 Choreo 创建项目", Colors.YELLOW)
        print(f"1. 访问：{self.console_url}")
        print("2. 点击 'Create' -> 'Project'")
        print("3. 输入项目名称：chatgpt2api")
        print("4. 选择项目类型：Multi-Repository")
        print()
        
        print_color("第三步：创建后端服务组件", Colors.YELLOW)
        print("1. 在项目中点击 'Create' -> 'Service'")
        print("2. 组件名称：chatgpt2api-backend")
        print("3. 选择 'GitHub' 作为代码源")
        print("4. 授权并选择你的仓库")
        print("5. 分支：main")
        print("6. Buildpack：Docker")
        print("7. Dockerfile 路径：./Dockerfile")
        print("8. 端口：80")
        print()
        
        print_color("第四步：配置环境变量", Colors.YELLOW)
        print("在组件设置中添加环境变量：")
        print("  - CHATGPT2API_AUTH_KEY = chatgpt2api")
        print("  - STORAGE_BACKEND = json")
        print()
        
        print_color("第五步：构建和部署", Colors.YELLOW)
        print("1. 点击 'Build' 触发构建")
        print("2. 等待构建完成（可能需要几分钟）")
        print("3. 构建成功后，点击 'Deploy' 部署到 Development 环境")
        print("4. 等待部署完成")
        print()
        
        print_color("第六步：获取访问 URL", Colors.YELLOW)
        print("1. 部署完成后，在组件详情页查看 URL")
        print("2. 测试 API：访问 <URL>/v1/models")
        print()
        
        print_color("第七步：创建前端组件（可选）", Colors.YELLOW)
        print("1. 创建新组件：chatgpt2api-frontend")
        print("2. 类型：Web Application")
        print("3. 使用相同的 GitHub 仓库")
        print("4. 构建路径：./web")
        print("5. 构建命令：npm install && npm run build")
        print("6. 启动命令：npm start")
        print("7. 端口：3000")
        print()
        
    def show_github_action_setup(self):
        """显示 GitHub Actions 设置"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("GitHub Actions 自动部署设置", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        print_color("步骤 1: 获取 Choreo Token", Colors.YELLOW)
        print(f"1. 访问：{self.console_url}/settings/tokens")
        print("2. 创建新的 Personal Access Token")
        print("3. 复制 Token（只显示一次）")
        print()
        
        print_color("步骤 2: 配置 GitHub Secrets", Colors.YELLOW)
        print("1. 进入 GitHub 仓库 -> Settings -> Secrets and variables -> Actions")
        print("2. 添加以下 Secrets：")
        print("   - Name: CHOREO_TOKEN")
        print("     Value: <你的 Choreo Token>")
        print()
        print("   - Name: CHATGPT2API_AUTH_KEY")
        print("     Value: chatgpt2api (或自定义)")
        print()
        
        print_color("步骤 3: 触发部署", Colors.YELLOW)
        print("1. 推送代码到 main 分支：")
        print("   git add .")
        print("   git commit -m 'Deploy to Choreo'")
        print("   git push origin main")
        print()
        print("2. 或在 GitHub Actions 页面手动触发工作流")
        print()
        
    def show_alternative_platforms(self):
        """显示替代平台"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("替代部署平台", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        print("如果 Choreo 部署遇到困难，可以考虑以下平台：")
        print()
        
        print_color("1. Railway.app", Colors.GREEN)
        print("   - 支持 Docker 和 Dockerfile")
        print("   - 免费额度：500 小时/月")
        print("   - 部署命令：railway up")
        print()
        
        print_color("2. Render.com", Colors.GREEN)
        print("   - 支持 Docker 部署")
        print("   - 免费层可用")
        print("   - Web 界面简单易用")
        print()
        
        print_color("3. Fly.io", Colors.GREEN)
        print("   - 优秀的 Docker 支持")
        print("   - 免费额度充足")
        print("   - 部署命令：fly deploy")
        print()
        
        print_color("4. Heroku", Colors.GREEN)
        print("   - 经典 PaaS 平台")
        print("   - 支持 Docker")
        print("   - 部署命令：git push heroku main")
        print()
        
    def generate_deployment_files(self):
        """生成部署所需的额外文件"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("生成部署文件", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        # 检查必要文件
        files_to_check = [
            'Dockerfile',
            'requirements.txt',
            '.github/workflows/choreo-deploy.yml',
            '.choreo/component.yaml'
        ]
        
        print("检查部署文件：")
        all_exist = True
        for file in files_to_check:
            if os.path.exists(file):
                print_success(f"{file} 存在")
            else:
                print_error(f"{file} 不存在")
                all_exist = False
        
        if all_exist:
            print()
            print_success("所有部署文件已就绪！")
        else:
            print()
            print_error("部分文件缺失，请检查项目结构")
        
        print()
        
    def run(self):
        """运行部署流程"""
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("ChatGPT2API Choreo 部署助手", Colors.YELLOW)
        print_color("="*60, Colors.BLUE)
        print()
        
        # 显示认证说明
        self.get_auth_instructions()
        
        # 显示部署方案
        self.show_docker_deployment_guide()
        
        # 询问用户选择
        print()
        print_color("请选择部署方式：", Colors.YELLOW)
        print("1. 查看手动部署详细步骤")
        print("2. 查看 GitHub Actions 自动部署设置")
        print("3. 查看替代部署平台")
        print("4. 检查部署文件")
        print("5. 退出")
        print()
        
        try:
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == '1':
                self.show_manual_deployment_steps()
            elif choice == '2':
                self.show_github_action_setup()
            elif choice == '3':
                self.show_alternative_platforms()
            elif choice == '4':
                self.generate_deployment_files()
            elif choice == '5':
                print_info("退出部署助手")
                return
            else:
                print_error("无效选项")
                return
            
            # 显示下一步
            print()
            print_color("="*60, Colors.BLUE)
            print_color("下一步", Colors.YELLOW)
            print_color("="*60, Colors.BLUE)
            print()
            print("1. 按照上述步骤在 Choreo 控制台操作")
            print("2. 或将代码推送到 GitHub 并使用 GitHub Actions")
            print("3. 部署完成后，访问提供的 URL 测试 API")
            print()
            print_color("需要帮助？查看完整文档：", Colors.YELLOW)
            print("  - CHOREO_DEPLOYMENT.md")
            print("  - 部署到Choreo说明.md")
            print()
            
        except KeyboardInterrupt:
            print()
            print_info("用户取消操作")
            return

def main():
    """主函数"""
    deployer = ChoreoDeployer()
    deployer.run()

if __name__ == "__main__":
    main()
