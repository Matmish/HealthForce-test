import json
import re
import time
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError
from utils import json_logger, paced_wait, parse_date, ensure_outdir

OUT_FILE = Path("out/li_posts.json")


async def extract_posts(page, min_posts=5, timeout=60):
    posts = []
    start = time.time()

    while len(posts) < min_posts and (time.time() - start) < timeout:
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await paced_wait()
        posts = await page.query_selector_all("div.feed-shared-update-v2")

    results = []
    for post in posts:
        try:
            post_id = await post.get_attribute("data-urn") or ""
            author = await (
                await post.query_selector("span.feed-shared-actor__name")
            ).inner_text()
            date_el = await post.query_selector(
                "span.feed-shared-actor__sub-description"
            )
            posted_at = parse_date(await date_el.inner_text()) if date_el else None
            text_el = await post.query_selector(
                "div.feed-shared-update-v2__description"
            )
            text = (await text_el.inner_text()) if text_el else ""
            hashtags = re.findall(r"#(\w+)", text)
            links = re.findall(r"https?://\S+", text)
            reactions_el = await post.query_selector(
                "span.social-details-social-counts__reactions-count"
            )
            comments_el = await post.query_selector(
                "span.social-details-social-counts__comments"
            )
            reactions = (
                int((await reactions_el.inner_text()) or 0) if reactions_el else 0
            )
            comments = int((await comments_el.inner_text()) or 0) if comments_el else 0

            results.append(
                {
                    "post_id": post_id,
                    "author_name": author.strip(),
                    "posted_at": posted_at,
                    "text": text.strip(),
                    "hashtags": hashtags,
                    "links": links,
                    "reactions_count": reactions,
                    "comments_count": comments,
                }
            )
        except Exception as e:
            json_logger("LI_POST_PARSE_FAIL", str(e))

    return results


async def run_linkedin_extractor(profile_url: str, min_posts: int):
    ensure_outdir()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=".auth/li_storage_state.json")
        page = await context.new_page()

        json_logger("LI_NAV_START", {"url": profile_url})
        try:
            await page.goto(profile_url + "recent-activity/shares/")
            posts = await extract_posts(page, min_posts)
        except TimeoutError:
            json_logger("LI_TIMEOUT", {"url": profile_url})
            posts = []
        finally:
            await browser.close()

    out = {
        "profile_url": profile_url,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_posts": len(posts),
        "posts": posts,
    }

    OUT_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    json_logger("LI_SAVED", {"file": str(OUT_FILE), "count": len(posts)})
