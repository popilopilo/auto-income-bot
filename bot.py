import os, requests, datetime, re
from requests_oauthlib import OAuth1

# ── Keys ─────────────────────────────────────────────────────────────────────
GROQ_API_KEY         = os.environ["GROQ_API_KEY"]
STRIPE_SECRET_KEY    = os.environ["STRIPE_SECRET_KEY"]
STRIPE_PRICE_ID      = os.environ["STRIPE_PRICE_ID"]
SITE_URL             = os.environ["SITE_URL"]
DEVTO_API_KEY        = os.environ["DEVTO_API_KEY"]
TUMBLR_CONSUMER_KEY  = os.environ["TUMBLR_CONSUMER_KEY"]
TUMBLR_CONSUMER_SECRET = os.environ["TUMBLR_CONSUMER_SECRET"]
TUMBLR_OAUTH_TOKEN   = os.environ["TUMBLR_OAUTH_TOKEN"]
TUMBLR_OAUTH_SECRET  = os.environ["TUMBLR_OAUTH_SECRET"]
TUMBLR_BLOG_NAME     = os.environ["TUMBLR_BLOG_NAME"]

# ── Topics ────────────────────────────────────────────────────────────────────
TOPICS = [
    ("10 Proven Ways to Save $500 This Month",          "personal finance, saving money, budgeting"),
    ("The Beginner's Guide to Deep, Restful Sleep",     "sleep, health, wellness, self improvement"),
    ("Work From Home Productivity: The Complete Guide", "productivity, work from home, focus"),
    ("10-Minute Daily Workout That Actually Works",     "fitness, exercise, health, workout"),
    ("Meal Prep Mastery: Eat Well All Week for $30",    "meal prep, food, budget cooking, healthy eating"),
    ("How to Start Investing With Just $50",            "investing, personal finance, money, beginners"),
    ("The Ultimate Guide to Stress-Free Mornings",      "morning routine, productivity, self improvement"),
    ("7 Habits of People Who Never Worry About Money",  "money, finance, habits, self improvement"),
]

today = datetime.date.today()
topic, tags = TOPICS[today.toordinal() % len(TOPICS)]

# ── Groq AI ───────────────────────────────────────────────────────────────────
def groq(prompt, tokens=1200):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile",
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": tokens}
    )
    resp = r.json()
    if "choices" not in resp:
        raise Exception(f"Groq error: {resp}")
    return resp["choices"][0]["message"]["content"]

print("🤖 Generating content...")
guide       = groq(f"Write a detailed, practical, engaging guide titled '{topic}'. Use emoji section headers. Be specific and actionable. Around 800 words.")
tagline     = groq(f"Write ONE punchy marketing tagline under 12 words for a guide called '{topic}'. No quotes, no punctuation at end.", 60)
bullets_raw = groq(f"List exactly 5 bullet points of what someone learns from '{topic}'. Each under 10 words. One per line, no numbers, no dashes, no bullets.", 200)
seo_desc    = groq(f"Write a compelling meta description under 155 characters for '{topic}'.", 80)
devto_intro = groq(f"Write a short 3-paragraph blog intro (no title) for '{topic}' that gives real value and ends by mentioning a full guide at {SITE_URL}. Sound helpful and human.", 400)
tumblr_post = groq(f"Write a short Tumblr post (2 paragraphs, casual tone) about '{topic}' with a link to read more at {SITE_URL}. End with relevant hashtags.", 300)

bullet_list = [b.strip("•-– \t") for b in bullets_raw.strip().split("\n") if b.strip()][:5]

# ── Stripe ────────────────────────────────────────────────────────────────────
print("💳 Creating Stripe payment link...")
stripe_resp = requests.post(
    "https://api.stripe.com/v1/payment_links",
    auth=(STRIPE_SECRET_KEY, ""),
    data={"line_items[0][price]": STRIPE_PRICE_ID,
          "line_items[0][quantity]": 1,
          "after_completion[type]": "redirect",
          "after_completion[redirect][url]": SITE_URL}
).json()
stripe_url = stripe_resp.get("url", "#")
if stripe_url == "#":
    print(f"⚠️ Stripe warning: {stripe_resp}")

# ── Markdown → HTML ───────────────────────────────────────────────────────────
def md_to_html(text):
    lines, out = text.split("\n"), []
    for line in lines:
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        if line.startswith("## ") or line.startswith("### "):
            out.append(f"<h2>{line.lstrip('#').strip()}</h2>")
        elif line.strip():
            out.append(f"<p>{line}</p>")
    return "\n".join(out)

paragraphs   = [p for p in guide.split("\n") if p.strip()]
preview_html = md_to_html("\n".join(paragraphs[:5]))
locked_html  = md_to_html("\n".join(paragraphs[5:]))
bullets_html = "\n".join(f"<li>✅ {b}</li>" for b in bullet_list)

# ── Landing Page ──────────────────────────────────────────────────────────────
print("🌐 Building landing page...")
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{seo_desc}"/>
  <meta property="og:title" content="{topic}"/>
  <meta property="og:description" content="{seo_desc}"/>
  <title>{topic} | Daily Guides</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --purple: #7c3aed; --purple-dark: #5b21b6; --purple-light: #ede9fe;
      --gold: #f59e0b; --text: #1e1b4b; --muted: #6b7280; --bg: #f8fafc;
    }}
    body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }}

    .hero {{
      background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #7c3aed 100%);
      color: white; padding: 90px 24px 110px; text-align: center; position: relative; overflow: hidden;
    }}
    .hero::before {{
      content: ''; position: absolute; inset: 0; opacity: 0.04;
      background-image: radial-gradient(circle, #fff 1px, transparent 1px);
      background-size: 32px 32px;
    }}
    .badge {{
      display: inline-block; background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.5);
      color: #fde68a; padding: 6px 18px; border-radius: 999px; font-size: 12px;
      font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 28px;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 5vw, 3.6rem); font-weight: 900; line-height: 1.12;
      max-width: 820px; margin: 0 auto 20px; letter-spacing: -0.025em;
    }}
    .hero h1 em {{ color: #fde68a; font-style: normal; }}
    .tagline {{ font-size: clamp(1rem, 2vw, 1.2rem); opacity: 0.8; max-width: 540px; margin: 0 auto 44px; }}
    .hero-cta {{
      display: inline-block; background: var(--gold); color: #1c1400;
      padding: 20px 52px; border-radius: 14px; font-size: 1.15rem; font-weight: 800;
      text-decoration: none; transition: all .25s; box-shadow: 0 8px 32px rgba(245,158,11,0.45);
      position: relative; z-index: 1;
    }}
    .hero-cta:hover {{ transform: translateY(-4px); box-shadow: 0 16px 48px rgba(245,158,11,0.55); }}
    .hero-sub {{ margin-top: 18px; font-size: 0.82rem; opacity: 0.55; letter-spacing: 0.03em; }}

    .trust {{
      background: white; border-bottom: 1px solid #e5e7eb;
      display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;
      padding: 18px 24px; font-size: 0.85rem; color: var(--muted); font-weight: 600;
    }}
    .trust span {{ display: flex; align-items: center; gap: 7px; }}

    .wrap {{ max-width: 780px; margin: 0 auto; padding: 72px 24px; }}
    .label {{
      text-align: center; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em;
      text-transform: uppercase; color: var(--purple); margin-bottom: 10px;
    }}
    .wrap h2 {{
      text-align: center; font-size: clamp(1.6rem, 3vw, 2.3rem);
      font-weight: 800; line-height: 1.2; margin-bottom: 36px; letter-spacing: -0.02em;
    }}

    .learn {{
      background: var(--purple-light); border: 2px solid #c4b5fd;
      border-radius: 18px; padding: 40px 44px;
    }}
    .learn ul {{ list-style: none; display: flex; flex-direction: column; gap: 16px; }}
    .learn li {{ font-size: 1.05rem; font-weight: 500; }}

    .card {{
      background: white; border-radius: 20px; padding: 52px;
      box-shadow: 0 4px 32px rgba(0,0,0,0.07); border: 1px solid #f0f0f0;
    }}
    .card h2 {{ font-size: 1.25rem; color: var(--purple); font-weight: 700; margin-bottom: 12px; text-align:left; }}
    .card p {{ color: #374151; margin-bottom: 12px; }}
    .blur-zone {{ position: relative; margin-top: 4px; }}
    .blurred {{ filter: blur(6px); user-select: none; pointer-events: none; opacity: 0.5; max-height: 160px; overflow: hidden; }}
    .blur-fade {{
      position: absolute; bottom: 0; left: 0; right: 0; height: 100px;
      background: linear-gradient(transparent, white);
    }}
    .lock-msg {{ text-align: center; margin-top: 20px; color: var(--muted); font-size: 0.9rem; font-weight: 500; }}

    .cta-box {{
      background: linear-gradient(135deg, #1e1b4b, #5b21b6);
      color: white; border-radius: 24px; padding: 64px 52px; text-align: center;
      box-shadow: 0 24px 64px rgba(91,33,182,0.35);
    }}
    .cta-box h2 {{ color: white; margin-bottom: 6px; }}
    .price {{ font-size: 4rem; font-weight: 900; color: #fde68a; line-height: 1; margin: 18px 0 4px; }}
    .price-note {{ opacity: 0.65; font-size: 0.88rem; margin-bottom: 36px; }}
    .buy-btn {{
      display: inline-block; background: var(--gold); color: #1c1400;
      padding: 22px 64px; border-radius: 14px; font-size: 1.2rem; font-weight: 800;
      text-decoration: none; transition: all .25s; box-shadow: 0 8px 32px rgba(245,158,11,0.5);
      width: 100%; max-width: 420px;
    }}
    .buy-btn:hover {{ transform: translateY(-4px); box-shadow: 0 16px 48px rgba(245,158,11,0.6); }}
    .secure {{ margin-top: 18px; font-size: 0.82rem; opacity: 0.6; }}

    .urgency {{
      background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px;
      padding: 14px 20px; text-align: center; font-size: 0.88rem;
      font-weight: 600; color: #92400e; margin-top: 24px;
    }}

    footer {{ text-align: center; padding: 44px 24px; font-size: 0.78rem; color: var(--muted); border-top: 1px solid #e5e7eb; }}

    @media(max-width:600px) {{
      .trust {{ gap: 16px; font-size: 0.78rem; }}
      .cta-box, .card, .learn {{ padding: 28px 20px; }}
      .price {{ font-size: 3rem; }}
    }}
  </style>
</head>
<body>

<section class="hero">
  <div class="badge">📘 Today's Featured Guide — {today.strftime('%B %d, %Y')}</div>
  <h1>{topic}</h1>
  <p class="tagline">{tagline}</p>
  <a href="{stripe_url}" class="hero-cta">Get Instant Access — $4.99 →</a>
  <p class="hero-sub">⚡ Instant access &nbsp;·&nbsp; 📱 Read on any device &nbsp;·&nbsp; ✅ One-time payment</p>
</section>

<div class="trust">
  <span>🔒 Secure Checkout</span>
  <span>⚡ Instant Access</span>
  <span>💳 Powered by Stripe</span>
  <span>📘 New guide every day</span>
</div>

<div class="wrap">
  <p class="label">What's inside</p>
  <h2>Here's exactly what you'll learn</h2>
  <div class="learn"><ul>{bullets_html}</ul></div>
</div>

<div class="wrap" style="padding-top:0">
  <p class="label">Free preview</p>
  <h2>Read the opening — free</h2>
  <div class="card">
    {preview_html}
    <div class="blur-zone">
      <div class="blurred">{locked_html[:800]}</div>
      <div class="blur-fade"></div>
    </div>
    <p class="lock-msg">🔒 The rest is locked. Unlock the full guide below.</p>
  </div>
</div>

<div class="wrap" style="padding-top:0">
  <div class="cta-box">
    <p style="font-size:0.78rem;opacity:0.6;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">Full guide</p>
    <h2>{topic}</h2>
    <div class="price">$4.99</div>
    <p class="price-note">One-time · Instant access · No subscription ever</p>
    <a href="{stripe_url}" class="buy-btn">🔓 Unlock Full Guide Now →</a>
    <p class="secure">🛡️ 100% secure · Powered by Stripe · Money-back if unsatisfied</p>
  </div>
  <div class="urgency">⏰ This guide rotates daily — a new topic publishes tomorrow!</div>
</div>

<footer>
  © {today.year} Daily Guides &nbsp;·&nbsp; New guide published every day
  &nbsp;·&nbsp; <a href="mailto:support@dailyguides.com" style="color:inherit">Contact</a>
  <br><br>Published {today.strftime('%B %d, %Y')}
</footer>
</body></html>"""

os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("✅ Landing page saved")

# ── POST TO DEV.TO ────────────────────────────────────────────────────────────
print("📝 Posting to Dev.to...")
try:
    tag_list = [t.strip().replace(" ", "").lower() for t in tags.split(",")][:4]
    devto_body = f"{devto_intro}\n\n---\n\n*Want the full guide? [Read it here →]({SITE_URL})*"
    r = requests.post(
        "https://dev.to/api/articles",
        headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"},
        json={"article": {
            "title": topic,
            "body_markdown": devto_body,
            "published": True,
            "tags": tag_list,
            "canonical_url": SITE_URL
        }}
    )
    if r.status_code in [200, 201]:
        print(f"✅ Dev.to posted: {r.json().get('url', '')}")
    else:
        print(f"⚠️ Dev.to error {r.status_code}: {r.text[:200]}")
except Exception as e:
    print(f"⚠️ Dev.to exception: {e}")

# ── POST TO TUMBLR ────────────────────────────────────────────────────────────
print("📝 Posting to Tumblr...")
try:
    auth = OAuth1(TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET,
                  TUMBLR_OAUTH_TOKEN, TUMBLR_OAUTH_SECRET)
    tag_list_tumblr = [t.strip() for t in tags.split(",")]
    r = requests.post(
        f"https://api.tumblr.com/v2/blog/{TUMBLR_BLOG_NAME}.tumblr.com/post",
        auth=auth,
        json={{
            "type": "text",
            "title": topic,
            "body": tumblr_post.replace("\n", "<br>"),
            "tags": tag_list_tumblr
        }}
    )
    if r.status_code in [200, 201]:
        print("✅ Tumblr posted")
    else:
        print(f"⚠️ Tumblr error {r.status_code}: {r.text[:200]}")
except Exception as e:
    print(f"⚠️ Tumblr exception: {e}")

print(f"\n🎉 Done for {today}! Topic: '{topic}'")
