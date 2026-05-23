#!/usr/bin/env python3
"""
doc.py - AI-powered code comment generator
Usage: python doc.py <file.py> [--dry-run] [--replace]
"""

import subprocess
import sys
import os
import argparse
import requests
import json
from pathlib import Path


def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = value


def read_file(file_path):
    """Read Python file content"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def generate_comments(code_content):
    """Generate Chinese comments using AI"""
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("Error: MIMO_API_KEY environment variable not set")
        print("Set it with: export MIMO_API_KEY=your_api_key")
        sys.exit(1)

    base_url = os.environ.get("MIMO_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1")
    model = os.environ.get("MIMO_MODEL", "mimo-v2.5")

    # Truncate if too long
    if len(code_content) > 6000:
        code_content = code_content[:6000] + "\n... (truncated)"

    prompt = f"""分析以下 Python 代码，为关键代码添加中文注释。

要求：
1. 为每个函数/方法添加中文 docstring（如果还没有的话）
2. 为复杂的逻辑添加行内注释
3. 保留原有代码结构，只添加注释
4. 注释要简洁明了，适合中国开发者阅读
5. 不要修改代码逻辑

代码：
```python
{code_content}
```

输出格式：返回完整的代码，包含新增的注释。只返回代码，不要其他说明。"""

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 4000
        }
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Extract code from markdown block if present
        if "```python" in content:
            content = content.split("```python")[1]
            if "```" in content:
                content = content.split("```")[0]
        elif "```" in content:
            content = content.split("```")[1]
            if "```" in content:
                content = content.split("```")[0]

        return content.strip()
    except Exception as e:
        print(f"Error calling AI API: {e}")
        sys.exit(1)


def write_file(file_path, content):
    """Write content to file"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to: {file_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


def main():
    load_env_file()

    parser = argparse.ArgumentParser(description="AI-powered Python code comment generator")
    parser.add_argument("file", help="Python file to add comments")
    parser.add_argument("--dry-run", action="store_true", help="Show result without saving")
    parser.add_argument("--replace", action="store_true", help="Replace original file (default: create new file with _commented suffix)")
    args = parser.parse_args()

    # Check file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    if not file_path.suffix == ".py":
        print("Error: Only .py files are supported")
        sys.exit(1)

    # Read original code
    print(f"Reading: {file_path}")
    original_code = read_file(file_path)

    if not original_code.strip():
        print("Error: File is empty")
        sys.exit(1)

    # Generate comments
    print("Generating comments with AI...")
    commented_code = generate_comments(original_code)

    # Show preview
    print("\n" + "=" * 50)
    print("PREVIEW (first 50 lines):")
    print("=" * 50)
    for i, line in enumerate(commented_code.split("\n")[:50], 1):
        print(f"{i:3}: {line}")

    if args.dry_run:
        print("\n[DRY RUN] No changes saved")
        return

    # Save
    if args.replace:
        output_path = file_path
    else:
        output_path = file_path.with_name(f"{file_path.stem}_commented{file_path.suffix}")

    write_file(output_path, commented_code)
    print(f"\nDone! Comments added to: {output_path}")


if __name__ == "__main__":
    main()
