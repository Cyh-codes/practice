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
    """Load environment variables from .env file if it exists"""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                # Parse KEY=VALUE
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value


def get_git_diff():
    """Get staged and unstaged changes"""
    # Get unstaged changes (new/modified/deleted files)
    result = subprocess.run(
        ["git", "diff", "--stat"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    if result.returncode != 0:
        print(f"Error getting git diff: {result.stderr}")
        sys.exit(1)

    # Get detailed diff
    result_detail = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )

    # Also check for untracked files
    result_untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )

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
    """Generate commit message using mimo API"""
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("Error: MIMO_API_KEY environment variable not set")
        print("Set it with: export MIMO_API_KEY=your_api_key")
        sys.exit(1)

    base_url = os.environ.get("MIMO_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1")
    model = os.environ.get("MIMO_MODEL", "mimo-v2.5")

    # Build prompt
    prompt_parts = ["Generate a concise git commit message for the following changes:\n"]

    if diff_stat:
        prompt_parts.append(f"Changed files:\n{diff_stat}\n")

    if diff_detail:
        # Truncate if too long
        if len(diff_detail) > 4000:
            diff_detail = diff_detail[:4000] + "\n... (truncated)"
        prompt_parts.append(f"Diff details:\n{diff_detail}\n")

    if untracked_files:
        prompt_parts.append(f"New files: {', '.join(untracked_files)}\n")

    prompt_parts.append("""
Output a JSON object with a single key "message" containing the commit message.

Rules:
1. Use conventional commits format: type(scope): description
2. Types: feat, fix, docs, style, refactor, test, chore
3. Keep under 72 characters
4. Be specific about what changed""")

    prompt = "\n".join(prompt_parts)

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
            "temperature": 0.3,
            "max_tokens": 300,
            "response_format": {"type": "json_object"}
        }
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return json.loads(content)["message"]
    except Exception as e:
        print(f"Error calling mimo API: {e}")
        sys.exit(1)


def git_add_commit_push(message, dry_run=False, no_push=False):
    """Execute git add, commit, and push"""
    # Stage all changes
    if not dry_run:
        subprocess.run(["git", "add", "."], cwd=os.getcwd())

    # Commit
    if not dry_run:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            print(f"Commit failed: {result.stderr}")
            sys.exit(1)
        print(f"Committed: {message}")

    # Push
    if not dry_run and not no_push:
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        branch = result.stdout.strip()

        print(f"Pushing to {branch}...")
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode != 0:
            print(f"Push failed: {result.stderr}")
            sys.exit(1)
        print("Push successful!")


def main():
    # Load .env file if exists
    load_env_file()

    parser = argparse.ArgumentParser(description="AI-powered git commit tool")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--no-push", action="store_true", help="Commit only, don't push")
    parser.add_argument("-m", "--message", type=str, help="Use provided message instead of AI generation")
    args = parser.parse_args()

    # Check if in git repo
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    if result.returncode != 0:
        print("Error: Not a git repository")
        sys.exit(1)

    print("Analyzing changes...")
    diff = get_git_diff()

    if not diff.stat_output and not diff.untracked_files:
        print("No changes to commit")
        sys.exit(0)

    # Generate or use provided message
    if args.message:
        commit_message = args.message
    else:
        print("Generating commit message with AI...")
        commit_message = generate_commit_message(
            diff.stat_output,
            diff.detail_output,
            diff.untracked_files
        )

    print(f"\nCommit message: {commit_message}")

    if args.dry_run:
        print("\n[DRY RUN] Would execute:")
        print("  git add .")
        print(f"  git commit -m \"{commit_message}\"")
        print("  git push")
        return

    # Confirm
    confirm = input("\nProceed? (Y/n): ").strip().lower()
    if confirm and confirm != 'y':
        print("Cancelled")
        sys.exit(0)

    git_add_commit_push(commit_message, args.dry_run, args.no_push)


if __name__ == "__main__":
    main()
