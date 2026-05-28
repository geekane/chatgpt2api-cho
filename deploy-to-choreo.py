#!/usr/bin/env python3
"""
ChatGPT2API Choreo 部署脚本
使用 Choreo CLI 将项目部署到 Choreo 平台
"""

import subprocess
import sys
import json
import time
from typing import Optional

# 配置
PROJECT_NAME = "chatgpt2api"
BACKEND_COMPONENT = "chatgpt2api-backend"
FRONTEND_COMPONENT = "chatgpt2api-frontend"
ENVIRONMENT = "development"

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'

def print_color(message: str, color: str):
    """彩色输出"""
    print(f"{color}{message}{Colors.NC}")

def run_command(cmd: list, capture_output: bool = False) -> Optional[str]:
    """执行命令"""
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print_color(f"命令执行失败: {' '.join(cmd)}", Colors.RED)
        if capture_output and e.stderr:
            print(e.stderr)
        return None
    except FileNotFoundError:
        print_color(f"命令未找到: {cmd[0]}", Colors.RED)
        return None

def check_cli():
    """检查 Choreo CLI 是否安装"""
    print_color("检查 Choreo CLI...", Colors.YELLOW)
    result = run_command(["wdp", "--version"], capture_output=True)
    if result:
        print_color("✓ Choreo CLI 已安装", Colors.GREEN)
        return True
    else:
        print_color("✗ Choreo CLI 未安装", Colors.RED)
        print("请运行以下命令安装:")
        print("curl -o- https://raw.githubusercontent.com/wso2/wdp-cli/main/scripts/install.sh | bash")
        return False

def login():
    """登录 Choreo"""
    print_color("步骤 1: 登录 Choreo 平台", Colors.YELLOW)
    run_command(["wdp", "login"])

def create_project():
    """创建项目"""
    print_color("步骤 2: 创建项目", Colors.YELLOW)
    # 检查项目是否存在
    result = run_command(["wdp", "get", "project", PROJECT_NAME], capture_output=True)
    if result:
        print_color(f"✓ 项目 '{PROJECT_NAME}' 已存在", Colors.GREEN)
    else:
        print(f"创建新项目: {PROJECT_NAME}")
        run_command(["wdp", "create", "project", PROJECT_NAME, "--type=multi-repository"])
        print_color("✓ 项目创建成功", Colors.GREEN)

def create_component(component_name: str, component_type: str, language: str, buildpack: str):
    """创建组件"""
    result = run_command([
        "wdp", "get", "component", component_name,
        "--project", PROJECT_NAME
    ], capture_output=True)
    
    if result:
        print_color(f"✓ 组件 '{component_name}' 已存在", Colors.GREEN)
    else:
        print(f"创建组件: {component_name}")
        run_command([
            "wdp", "create", "component", component_name,
            "--project", PROJECT_NAME,
            "--type", component_type,
            "--language", language,
            "--buildpack", buildpack
        ])
        print_color(f"✓ 组件 '{component_name}' 创建成功", Colors.GREEN)

def set_env_var(component: str, key: str, value: str):
    """设置环境变量"""
    run_command([
        "wdp", "set", "env", component,
        "--project", PROJECT_NAME,
        "--env", ENVIRONMENT,
        "--key", key,
        "--value", value
    ])

def trigger_build(component: str) -> Optional[str]:
    """触发构建并返回构建 ID"""
    print(f"触发 {component} 构建...")
    result = run_command([
        "wdp", "create", "build", component,
        "--project", PROJECT_NAME,
        "--output", "json"
    ], capture_output=True)
    
    if result:
        try:
            build_data = json.loads(result)
            build_id = build_data.get("id")
            print(f"构建 ID: {build_id}")
            return build_id
        except json.JSONDecodeError:
            print_color("无法解析构建响应", Colors.RED)
            return None
    return None

def wait_for_build(component: str, build_id: str) -> bool:
    """等待构建完成"""
    print("等待构建完成...")
    while True:
        result = run_command([
            "wdp", "get", "build", build_id,
            "--component", component,
            "--project", PROJECT_NAME,
            "--output", "json"
        ], capture_output=True)
        
        if result:
            try:
                build_data = json.loads(result)
                status = build_data.get("status")
                
                if status == "SUCCESS":
                    print_color("✓ 构建成功", Colors.GREEN)
                    return True
                elif status == "FAILED":
                    print_color("✗ 构建失败", Colors.RED)
                    return False
                else:
                    print(f"构建状态: {status}")
                    time.sleep(10)
            except json.JSONDecodeError:
                print_color("无法解析构建状态", Colors.RED)
                return False
        else:
            time.sleep(10)

def deploy_component(component: str, build_id: str):
    """部署组件"""
    print(f"部署 {component}...")
    run_command([
        "wdp", "create", "deployment", component,
        "--project", PROJECT_NAME,
        "--env", ENVIRONMENT,
        "--build-id", build_id
    ])
    print_color(f"✓ {component} 部署完成", Colors.GREEN)

def get_component_url(component: str) -> Optional[str]:
    """获取组件 URL"""
    result = run_command([
        "wdp", "get", "component", component,
        "--project", PROJECT_NAME,
        "--output", "json"
    ], capture_output=True)
    
    if result:
        try:
            component_data = json.loads(result)
            environments = component_data.get("environments", [])
            for env in environments:
                if env.get("name") == ENVIRONMENT:
                    return env.get("url")
        except json.JSONDecodeError:
            pass
    return None

def main():
    """主函数"""
    print_color("=== ChatGPT2API Choreo 部署脚本 ===", Colors.GREEN)
    
    # 检查 CLI
    if not check_cli():
        sys.exit(1)
    
    # 登录
    login()
    
    # 创建项目
    create_project()
    
    # 创建后端组件
    print_color("步骤 3: 创建后端服务组件", Colors.YELLOW)
    create_component(BACKEND_COMPONENT, "service", "python", "python")
    
    # 创建前端组件
    print_color("步骤 4: 创建前端 Web 应用组件", Colors.YELLOW)
    create_component(FRONTEND_COMPONENT, "web-application", "nodejs", "nodejs")
    
    # 配置环境变量
    print_color("步骤 5: 配置环境变量", Colors.YELLOW)
    auth_key = input("请输入 CHATGPT2API_AUTH_KEY (默认: chatgpt2api): ").strip()
    auth_key = auth_key or "chatgpt2api"
    set_env_var(BACKEND_COMPONENT, "CHATGPT2API_AUTH_KEY", auth_key)
    print_color("✓ 环境变量配置完成", Colors.GREEN)
    
    # 构建和部署后端
    print_color("步骤 6: 构建后端服务", Colors.YELLOW)
    backend_build_id = trigger_build(BACKEND_COMPONENT)
    if not backend_build_id:
        print_color("后端构建触发失败", Colors.RED)
        sys.exit(1)
    
    if not wait_for_build(BACKEND_COMPONENT, backend_build_id):
        sys.exit(1)
    
    print_color("步骤 7: 部署后端服务", Colors.YELLOW)
    deploy_component(BACKEND_COMPONENT, backend_build_id)
    
    # 获取后端 URL
    backend_url = get_component_url(BACKEND_COMPONENT)
    if backend_url:
        print(f"后端 URL: {backend_url}")
        set_env_var(FRONTEND_COMPONENT, "NEXT_PUBLIC_API_URL", backend_url)
    
    # 构建和部署前端
    print_color("步骤 8: 构建前端应用", Colors.YELLOW)
    frontend_build_id = trigger_build(FRONTEND_COMPONENT)
    if not frontend_build_id:
        print_color("前端构建触发失败", Colors.RED)
        sys.exit(1)
    
    if not wait_for_build(FRONTEND_COMPONENT, frontend_build_id):
        sys.exit(1)
    
    print_color("步骤 9: 部署前端应用", Colors.YELLOW)
    deploy_component(FRONTEND_COMPONENT, frontend_build_id)
    
    # 获取前端 URL
    frontend_url = get_component_url(FRONTEND_COMPONENT)
    
    # 完成
    print()
    print_color("=== 部署完成 ===", Colors.GREEN)
    if backend_url:
        print(f"后端 API: {backend_url}")
    if frontend_url:
        print(f"前端应用: {frontend_url}")
    print()
    print("查看日志:")
    print(f"  后端: wdp logs application --component {BACKEND_COMPONENT} --project {PROJECT_NAME} --env {ENVIRONMENT} --follow")
    print(f"  前端: wdp logs application --component {FRONTEND_COMPONENT} --project {PROJECT_NAME} --env {ENVIRONMENT} --follow")

if __name__ == "__main__":
    main()
