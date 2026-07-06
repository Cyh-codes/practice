import requests
import pytest

def test_github_api():
    """测试 GitHub API 搜索功能的返回数据是否符合预期"""

    url = "https://api.github.com/search/repositories"
    url += "?q=computer"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    assert r.status_code == 200, f"期待值为200,实际是:{r.status_code}"
    response_dict = r.json()
    assert len(response_dict['items']) == 30, f"一般列表期待值是30,实际是:{len(response_dict['items'])}"
    assert response_dict['total_count'] > 10000, f"一般仓库期待值是大于35,实际是{response_dict['total_count']}"

    first_repo = response_dict['items'][0]
    assert first_repo['stargazers_count'] > 1000, f"一般首个仓库star数>1000, 实际是{first_repo['stargazers_count']}"

