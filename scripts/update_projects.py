"""Regenerate the '$ ls projects/' section of README.md from the user's public repos."""
import json
import re
import urllib.request

USERNAME = "iandrade1987"
EXCLUDE = {USERNAME.lower()}
STATS_HOST = "https://github-readme-stats-iandrade1987.vercel.app"
README = "README.md"


def fetch_repos():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USERNAME}/repos?type=public&sort=updated&per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": USERNAME},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def build_block(repos):
    cards = []
    for repo in repos:
        name = repo["name"]
        if repo.get("fork") or repo.get("archived"):
            continue
        if name.lower() in EXCLUDE:
            continue
        cards.append(
            f'  <a href="https://github.com/{USERNAME}/{name}">\n'
            f'    <img height="165" src="{STATS_HOST}/api/pin/?username={USERNAME}&repo={name}'
            f'&hide_border=true&bg_color=0D1117&title_color=39FF14&text_color=C9D1D9&icon_color=39FF14" />\n'
            f"  </a>"
        )

    if not cards:
        return "> Repositories are on their way — this section will list pinned projects once they're uploaded."

    return '<p align="center">\n' + "\n".join(cards) + "\n</p>"


def main():
    repos = fetch_repos()
    block = build_block(repos)

    with open(README, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"(<!-- PROJECTS:START -->\n).*?(\n<!-- PROJECTS:END -->)",
        lambda m: m.group(1) + block + m.group(2),
        content,
        flags=re.DOTALL,
    )

    if new_content != content:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated")
    else:
        print("No changes needed")


if __name__ == "__main__":
    main()
