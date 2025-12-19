import requests
import os

def fetch_github_stats(username, pat):
    headers = {"Authorization": f"bearer {pat}"}
    query = f"""
    query {{
      user(login: "{username}") {{
        issueComments(
          filterBy: {{createdAt: {{since: "2025-01-01T00:00:00Z", until: "2025-12-31T23:59:59Z"}}}}
        ) {{ totalCount }}
        pullRequestReviews(
          filterBy: {{createdAt: {{since: "2025-01-01T00:00:00Z", until: "2025-12-31T23:59:59Z"}}}}
        ) {{ totalCount }}
      }}
    }}
    """
    response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    data = response.json()
    comments = data["data"]["user"]["issueComments"]["totalCount"]
    reviews = data["data"]["user"]["pullRequestReviews"]["totalCount"]
    return {"comments": comments, "reviews": reviews}

if __name__ == "__main__":
    username = os.getenv("GITHUB_USERNAME")
    pat = os.getenv("USER_STAT_TOKEN")
    stats = fetch_github_stats(username, pat)
    with open("STATS.md", "w") as f:
        f.write(f"## 2025 年度统计\n- Patch Review 数：{stats['reviews']}\n- Comment 数：{stats['comments']}\n")
