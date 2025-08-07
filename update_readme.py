import requests

USERNAME = "shefa19"  # তোমার GitHub username
README_PATH = "README.md"

def get_language_stats(username):
    repos = requests.get(f"https://api.github.com/users/{username}/repos").json()
    lang_count = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        lang_url = repo["languages_url"]
        langs = requests.get(lang_url).json()
        for lang, bytes_count in langs.items():
            lang_count[lang] = lang_count.get(lang, 0) + bytes_count
    return lang_count

def generate_badges(lang_stats):
    total = sum(lang_stats.values())
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    badges = []
    for lang, count in sorted_langs[:4]:
        percent = round((count / total) * 100, 2)
        color = "blue" if lang == "C" else "yellow" if lang == "Python" else "lightgrey"
        badges.append(f"![{lang}](https://img.shields.io/badge/{lang}-{percent}%25-{color}?style=for-the-badge&logo={lang.lower()})")
    return "\n".join(badges)

def update_readme(badges):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find("## 📊 Language Usage Overview")
    end = content.find("---", start)
    new_section = f"## 📊 Language Usage Overview\n\n{badges}\n\n---"
    updated = content[:start] + new_section + content[end:]
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

lang_stats = get_language_stats(USERNAME)
badges = generate_badges(lang_stats)
update_readme(badges)
