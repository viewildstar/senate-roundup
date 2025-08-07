# main.py

# ─── Imports ─────────────────────────────
import json
from scripts.twitter_scraper import get_tweets
from scripts.facebook_scraper import get_facebook_posts
from scripts.news_scraper import get_articles
from scripts.topic_extractor import extract_topics

# ─── Function Definitions ────────────────
def format_summary_by_party(results: list[dict]) -> str:
    by_party = {"Republican": [], "Democrat": []}
    for r in results:
        top_items = [t[0] for t in r["topics"]][:15]
        keyword_str = ", ".join(top_items)
        line = f"**{r['senator'].split()[-1]}**: {keyword_str}"
        by_party[r["party"]].append(line)
    
    return (
        "# Senate Roundup – Week of August 1–7, 2025\n\n"
        "## Republicans\n\n" +
        "\n".join(by_party["Republican"]) +
        "\n\n## Democrats\n\n" +
        "\n".join(by_party["Democrat"])
    )

# ─── Main Logic ──────────────────────────
if __name__ == "__main__":
    import yaml

    with open("senators.yml") as f:
        senators = yaml.safe_load(f)

    results = []
    for senator in senators:
        tweets = get_tweets(senator["twitter"])
        posts = get_facebook_posts(senator["facebook"])
        news = get_articles(senator["name"])

        all_text = (
            "\n".join(t.content for t in tweets) +
            "\n".join(p["text"] for p in posts) +
            "\n".join(a["text"] for a in news)
        )

        topics = extract_topics(all_text)
        results.append({
            "senator": senator["name"],
            "party": senator["party"],
            "topics": topics
        })

    summary_md = format_summary_by_party(results)
    with open("output/weekly_roundup.md", "w") as f:
        f.write(summary_md)

