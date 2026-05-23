#!/usr/bin/env python3
"""
gcommit.py - AI-powered git commit tool
Usage: python gcommit.py [--dry-run] [--no-push]
"""

import subprocess
import sys
import os
import argparse
import requests
import json
from pathlib import Path


def load_env_file():
    """从项目根目录的 .env 文件加载环境变量"""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith("#"):
                    continue
                # 解析 KEY=VALUE 格式的行
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # 仅在环境变量不存在时才设置
                    if key not in os.environ:
                        os.environ[key] = value


def get_git_diff():
    """获取 git 仓库中暂存区和工作区的差异信息"""
    # 获取未暂存的更改（新文件、修改或删除的文件）
    result = subprocess.run(
        ["git", "diff", "--stat"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=os.getcwd()
    )
    if result.returncode != 0:
        print(f"Error getting git diff: {result.stderr}")
        sys.exit(1)

    # 获取差异的详细信息（具体代码变更）
    result_detail = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=os.getcwd()
    )

    # 同时检查未跟踪（新）的文件
    result_untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=os.getcwd()
    )

    # 处理未跟踪文件列表
    untracked = result_untracked.stdout.strip()
    if untracked:
        untracked_files = untracked.split("\n")
        result.stat_output = result.stdout
        result.detail_output = result_detail.stdout
        result.untracked_files = untracked_files
    else:
        result.stat_output = result.stdout
        result.detail_output = result_detail.stdout
        result.untracked_files = []

    return result


def generate_commit_message(diff_stat, diff_detail, untracked_files):
    """使用 MIMO API 根据差异信息生成 Git 提交消息"""
    # 从环境变量获取 API 配置
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("Error: MIMO_API_KEY environment variable not set")
        print("Set it with: export MIMO_API_KEY=your_api_key")
        sys.exit(1)

    base_url = os.environ.get("MIMO_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1")
    model = os.environ.get("MIMO_MODEL", "mimo-v2.5")

    # 构建发送给 AI 的提示词
    prompt_parts = ["Generate a concise git commit message for the following changes:\n"]

    if diff_stat:
        prompt_parts.append(f"Changed files:\n{diff_stat}\n")

    if diff_detail:
        # 如果差异详情过长，则进行截断，以符合 token 限制
        if len(diff_detail) > 4000:
            diff_detail = diff_detail[:4000] + "\n... (truncated)"
        prompt_parts.append(f"Diff details:\n{diff_detail}\n")

    if untracked_files:
        prompt_parts.append(f"New files: {', '.join(untracked_files)}\n")

    # 添加提交消息的格式和规则要求
    prompt_parts.append("""
Output a JSON object with a single key "message" containing the commit message.

Rules:
1. Use conventional commits format: type(scope): description
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep under 72 characters
4. Be specific about what changed""")

    prompt = "\n".join(prompt_parts)

    try:
        # 设置 API 请求头和请求体
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 300,
            "response_format": {"type": "json_object"} # 要求返回 JSON 格式
        }
        # 发送 POST 请求调用 AI API
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        # 从 API 返回的 JSON 中提取生成的提交消息
        content = result["choices"][0]["message"]["content"]
        return json.loads(content)["message"]
    except Exception as e:
        print(f"Error calling mimo API: {e}")
        sys.exit(1)


def git_add_commit_push(message, dry_run=False, no_push=False):
    """执行 git add, commit 和 push 操作"""
    # 将所有更改添加到暂存区
    if not dry_run:
        subprocess.run(["git", "add", "."], cwd=os.getcwd())

    # 执行提交
    if not dry_run:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            print(f"Commit failed: {result.stderr}")
            sys.exit(1)
        print(f"Committed: {message}")

    # 推送到远程仓库（除非指定了 no_push 或处于试运行模式）
    if not dry_run and not no_push:
        # 获取当前分支名，以便推送到对应的远程分支
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=os.getcwd()
        )
        branch = result.stdout.strip()

        print(f"Pushing to {branch}...")
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            print(f"Push failed: {result.stderr}")
            sys.exit(1)
        print("Push successful!")


def main():
    # 主函数，程序入口
    # 加载 .env 文件中的环境变量
    load_env_file()

    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="AI-powered git commit tool")
    parser.add_argument("--dry-run", action="store_true", help="试运行模式，仅显示操作但不执行")
    parser.add_argument("--no-push", action="store_true", help="提交后不自动推送到远程仓库")
    args = parser.parse_args()

    # 获取当前工作目录的 git 差异
    diff_result = get_git_diff()

    # 使用 AI 根据差异生成提交消息
    commit_message = generate_commit_message(
        diff_result.stat_output,
        diff_result.detail_output,
        diff_result.untracked_files
    )

    print(f"Generated commit message:\n{commit_message}\n")

    # 执行实际的 git 操作（除非是试运行模式）
    git_add_commit_push(commit_message, dry_run=args.dry_run, no_push=args.no_push)


if __name__ == "__main__":
    main()