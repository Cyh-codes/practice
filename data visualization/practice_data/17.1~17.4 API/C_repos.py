import requests
import json

# 执行API调用并存储响应
url = "https://api.github.com/search/repositories"
url += "?q=language:Java+sort:stars+stars:>15000"

headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"Status Code: {r.status_code}")

# 将响应转换成字典
response_dict = r.json()
print(f"Total repositories: {response_dict['total_count']}")
print(f"Complete results: {not response_dict['incomplete_results']}")

# 探索相关的仓库的信息
repo_dicts = response_dict['items']
print(f"Repositories returned: {len(repo_dicts)}")

for repo_dict in repo_dicts:
    print("\nSelected information about repository:")
    print(f"Name: {repo_dict['name']}")
    print(f"Owner: {repo_dict['owner']['login']}")
    print(f"Stars: {repo_dict['stargazers_count']}")
    print(f"Respository: {repo_dict['created_at']}")
    print(f"Updated: {repo_dict['created_at']}")
    print(f"Description: {repo_dict['description']}")



