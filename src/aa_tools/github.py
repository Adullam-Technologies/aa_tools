"""Talk to GitHub (public info, no key needed for light use)."""

from __future__ import annotations

from ._http import request

GITHUB = "https://api.github.com"


def github_repo(repo: str, *, api_key: str | None = None):
    """Get info about a GitHub repository, e.g. ``"octocat/Hello-World"``.

    Example
    -------
    >>> info = aa.github_repo("pallets/flask")
    >>> print(info["stars"], "stars")
    """
    headers = {"Accept": "application/vnd.github+json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = request(f"{GITHUB}/repos/{repo}", headers=headers)
    return {
        "name": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "language": data.get("language"),
        "url": data.get("html_url"),
        "open_issues": data.get("open_issues_count"),
    }


def github_user(username: str, *, api_key: str | None = None):
    """Get public profile info for a GitHub user."""
    headers = {"Accept": "application/vnd.github+json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = request(f"{GITHUB}/users/{username}", headers=headers)
    return {
        "login": data.get("login"),
        "name": data.get("name"),
        "bio": data.get("bio"),
        "followers": data.get("followers"),
        "public_repos": data.get("public_repos"),
        "url": data.get("html_url"),
    }


def github_search_repos(query: str, *, count: int = 5, api_key: str | None = None):
    """Search GitHub repositories by keyword."""
    headers = {"Accept": "application/vnd.github+json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = request(f"{GITHUB}/search/repositories", params={"q": query, "per_page": count}, headers=headers)
    return [
        {
            "name": r.get("full_name"),
            "description": r.get("description"),
            "stars": r.get("stargazers_count"),
            "url": r.get("html_url"),
        }
        for r in data.get("items", [])
    ]
