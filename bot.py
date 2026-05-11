import os, requests, datetime, re, random, json, hashlib
from requests_oauthlib import OAuth1

# ── Keys ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY           = os.environ["GROQ_API_KEY"]
SITE_URL               = os.environ["SITE_URL"]
DEVTO_API_KEY          = os.environ["DEVTO_API_KEY"]
TUMBLR_CONSUMER_KEY    = os.environ["TUMBLR_CONSUMER_KEY"]
TUMBLR_CONSUMER_SECRET = os.environ["TUMBLR_CONSUMER_SECRET"]
TUMBLR_OAUTH_TOKEN     = os.environ["TUMBLR_OAUTH_TOKEN"]
TUMBLR_OAUTH_SECRET    = os.environ["TUMBLR_OAUTH_SECRET"]
TUMBLR_BLOG_NAME       = os.environ["TUMBLR_BLOG_NAME"]
STRIPE_SINGLE_URL      = os.environ["STRIPE_SINGLE_URL"]
STRIPE_SUB_URL         = os.environ["STRIPE_SUB_URL"]
FORMSPREE_ID           = os.environ["FORMSPREE_ID"]

GUIDE_KEY    = "dg7x9k2m"
SUB_SALT     = "dailyguides2026"
today        = datetime.date.today()
DATE_STR     = today.strftime("%Y-%m-%d")
GUIDE_URL    = f"{SITE_URL}/guides/{DATE_STR}.html"
REDIRECT_URL = f"{SITE_URL}/redirect.html?key={GUIDE_KEY}"

def make_sub_code(email):
    """Generate unique subscriber code from email."""
    raw = f"{SUB_SALT}{email.lower().strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]

# ── Topics ────────────────────────────────────────────────────────────────────
TOPICS = [
    ("How I Cut My Grocery Bill in Half Without Coupons", "personalfinance, savingmoney, budgeting, frugal"),
    ("The Sleep Routine That Changed Everything for Me", "sleep, health, wellness, selfimprovement"),
    ("Working From Home Without Losing Your Mind", "productivity, workfromhome, focus, remotework"),
    ("The 10-Minute Morning Workout You'll Actually Stick To", "fitness, exercise, health, workout"),
    ("Eating Well on $30 a Week: A Real Meal Plan", "mealprep, food, budgetcooking, healthyeating"),
    ("How to Start Investing When You Know Nothing", "investing, personalfinance, money, beginners"),
    ("The Morning Routine That Makes Everything Easier", "morningroutine, productivity, selfimprovement, wellness"),
    ("Small Money Habits That Add Up to Big Savings", "money, finance, habits, selfimprovement"),
    ("How to Actually Wake Up Early Without Hating It", "sleep, morningroutine, habits, wellness"),
    ("The Beginner's Guide to Meal Planning That Works", "mealprep, food, healthyeating, budgeting"),
    ("How to Stop Procrastinating for Good", "productivity, habits, selfimprovement, focus"),
    ("A Simple Guide to Paying Off Debt Faster", "personalfinance, debt, money, budgeting"),
    ("How to Build a Reading Habit You Actually Keep", "selfimprovement, habits, learning, productivity"),
    ("The No-Gym Fitness Plan That Gets Real Results", "fitness, health, exercise, noequipment"),
    ("How to Cook Healthy Meals When You're Always Tired", "food, healthyeating, mealprep, cooking"),
    ("A Beginner's Guide to Index Funds", "investing, finance, money, beginners"),
    ("How to Declutter Your Home Without the Overwhelm", "minimalism, organization, lifestyle, homeimprovement"),
    ("The Simple Budget System That Finally Worked for Me", "budgeting, personalfinance, money, savings"),
    ("How to Build Confidence in Any Situation", "selfimprovement, confidence, mindset, personaldevelopment"),
    ("The Honest Guide to Starting a Side Hustle", "sidehustle, money, entrepreneurship, income"),
    ("How to Stop Impulse Buying Once and for All", "personalfinance, money, habits, budgeting"),
    ("A Realistic Guide to Losing Weight Without Dieting", "health, fitness, weightloss, wellness"),
    ("How to Make Your Apartment Feel Like a Home", "homeimprovement, interior, lifestyle, decor"),
    ("The Introvert's Guide to Networking Without Cringe", "career, networking, selfimprovement, confidence"),
    ("How to Negotiate a Higher Salary And Actually Win", "career, money, finance, professionaldevelopment"),
    ("A Simple System for Keeping Your Home Clean", "organization, cleaning, homeimprovement, habits"),
    ("How to Build an Emergency Fund From Zero", "personalfinance, savings, money, budgeting"),
    ("The Beginner's Guide to Meditation No App Required", "meditation, wellness, mindfulness, selfimprovement"),
    ("How to Drink Less Without Feeling Left Out", "health, wellness, lifestyle, habits"),
    ("A Practical Guide to Better Posture at Your Desk", "health, fitness, workfromhome, wellness"),
    ("How to Save for a Holiday Without Going Broke", "travel, savings, personalfinance, budgeting"),
    ("The Simple Anti-Anxiety Toolkit That Actually Helps", "mentalhealth, wellness, anxiety, selfimprovement"),
    ("How to Learn Any Skill Twice as Fast", "learning, productivity, selfimprovement, skills"),
    ("A Guide to Eating Out Without Ruining Your Budget", "food, budgeting, personalfinance, lifestyle"),
    ("How to Finally Get Organised at Home", "organization, productivity, homeimprovement, habits"),
    ("The Beginner's Guide to Running From Zero to 5K", "running, fitness, health, exercise"),
    ("How to Save Money on Your Monthly Bills", "personalfinance, savings, budgeting, money"),
    ("A No-Nonsense Guide to Better Skin on a Budget", "skincare, health, beauty, wellness"),
    ("How to Stop Checking Your Phone Every 5 Minutes", "productivity, habits, mentalhealth, focus"),
    ("The Practical Guide to Working Smarter Not Harder", "productivity, career, workfromhome, focus"),
    ("How to Travel Cheap Without Sacrificing Comfort", "travel, budgeting, savings, lifestyle"),
    ("A Beginner's Guide to Growing Your Own Food", "gardening, food, sustainability, lifestyle"),
    ("How to Build a Capsule Wardrobe on a Budget", "fashion, minimalism, budgeting, lifestyle"),
    ("The Guide to Cooking for One Without Waste", "food, cooking, mealprep, budgeting"),
    ("How to Make Friends as an Adult Without It Being Weird", "lifestyle, selfimprovement, confidence, socialskills"),
    ("A Simple Guide to Improving Your Credit Score", "personalfinance, credit, money, finance"),
    ("How to Get a Better Night Sleep Tonight", "sleep, health, wellness, selfimprovement"),
    ("The Realistic Guide to Working Out With No Motivation", "fitness, exercise, habits, selfimprovement"),
    ("How to Spend Less Time on Social Media", "productivity, mentalhealth, habits, focus"),
    ("A Guide to Cooking Cheap Delicious Meals Every Night", "food, budgeting, mealprep, cooking"),
    ("How to Set Goals You Actually Achieve", "selfimprovement, productivity, habits, goals"),
    ("The Beginner's Guide to Strength Training at Home", "fitness, exercise, health, hometraining"),
    ("How to Handle a Job Interview With Confidence", "career, confidence, professionaldevelopment, selfimprovement"),
    ("A Simple Plan for Getting Out of Your Comfort Zone", "selfimprovement, mindset, personaldevelopment, confidence"),
    ("How to Write Better Emails That Get Replies", "career, productivity, professionaldevelopment, writing"),
    ("The Lazy Person's Guide to Eating Healthier", "health, food, healthyeating, wellness"),
    ("How to Stop Worrying About Things You Cannot Control", "mentalhealth, wellness, mindfulness, selfimprovement"),
    ("A Guide to Saving Money on Groceries Every Week", "personalfinance, budgeting, food, savings"),
    ("How to Be More Productive in the Morning", "morningroutine, productivity, habits, selfimprovement"),
    ("The Simple Guide to Starting a Journal", "selfimprovement, wellness, habits, mentalhealth"),
    ("How to Build Muscle Without a Gym Membership", "fitness, exercise, health, hometraining"),
    ("A Beginner's Guide to Cooking from Scratch", "food, cooking, healthyeating, skills"),
    ("How to Find a Job You Actually Like", "career, selfimprovement, professionaldevelopment, lifestyle"),
    ("The Guide to Managing Stress Before It Manages You", "mentalhealth, stress, wellness, selfimprovement"),
    ("How to Build Better Habits That Actually Stick", "habits, selfimprovement, productivity, personaldevelopment"),
    ("A Simple Guide to Saving for Retirement Early", "investing, personalfinance, retirement, money"),
    ("How to Improve Your Focus in a Distracted World", "productivity, focus, habits, selfimprovement"),
    ("The Beginner's Guide to Yoga at Home", "yoga, fitness, wellness, health"),
    ("How to Deal With Difficult People at Work", "career, confidence, selfimprovement, professionaldevelopment"),
    ("A Practical Guide to Living Below Your Means", "personalfinance, minimalism, budgeting, lifestyle"),
    ("How to Cook Meal Prep That You Will Actually Eat", "mealprep, food, healthyeating, cooking"),
    ("The Guide to Feeling More Energised Every Day", "health, wellness, fitness, lifestyle"),
    ("How to Survive and Thrive Working Night Shifts", "health, sleep, lifestyle, wellness"),
    ("A Simple Guide to Decluttering Your Digital Life", "productivity, organization, minimalism, technology"),
    ("How to Stop Living Paycheck to Paycheck", "personalfinance, budgeting, money, savings"),
    ("How to Start Exercising When You Hate Exercise", "fitness, health, habits, selfimprovement"),
    ("A Beginner's Guide to Personal Finance in Your 20s", "personalfinance, money, budgeting, beginners"),
    ("How to Eat Healthy When You Have No Time", "healthyeating, food, mealprep, productivity"),
    ("The Practical Guide to Saying No Without Guilt", "selfimprovement, confidence, mentalhealth, boundaries"),
    ("How to Make the Most of a Small Living Space", "homeimprovement, minimalism, organization, lifestyle"),
    ("A Guide to Building a Daily Exercise Habit", "fitness, habits, health, selfimprovement"),
    ("How to Stop Feeling Overwhelmed by Your To-Do List", "productivity, mentalhealth, organization, selfimprovement"),
    ("How to Start Saving When You Think You Cannot Afford To", "personalfinance, savings, budgeting, money"),
    ("How to Build a Skincare Routine That Works", "skincare, health, wellness, beauty"),
    ("The Guide to Getting Your Finances in Order This Month", "personalfinance, budgeting, money, finance"),
    ("How to Stop Emotional Eating for Good", "health, mentalhealth, wellness, habits"),
    ("A Simple Plan to Improve Your Mental Health Daily", "mentalhealth, wellness, selfimprovement, habits"),
    ("How to Get Promoted Without Playing Office Politics", "career, professionaldevelopment, confidence, selfimprovement"),
    ("How to Make Your Weekends Actually Restorative", "lifestyle, wellness, mentalhealth, selfimprovement"),
    ("How to Stop Being So Hard on Yourself", "mentalhealth, selfimprovement, mindset, wellness"),
    ("The Practical Guide to Getting Fit After 40", "fitness, health, exercise, wellness"),
    ("How to Afford to Travel More Than You Think", "travel, personalfinance, savings, lifestyle"),
    ("A Simple Guide to Building Better Relationships", "relationships, selfimprovement, lifestyle, confidence"),
    ("How to Finally Stick to a Workout Routine", "fitness, habits, exercise, selfimprovement"),
    ("A Beginner's Guide to Cycling for Fitness", "cycling, fitness, health, exercise"),
    ("How to Deal With Loneliness Without Feeling Pathetic", "mentalhealth, lifestyle, selfimprovement, wellness"),
    ("The Guide to Eating Well When You Hate Cooking", "food, healthyeating, cooking, lifestyle"),
    ("How to Be More Present in Your Daily Life", "mindfulness, wellness, selfimprovement, habits"),
    ("A Simple Guide to Managing Your Time Better", "productivity, timemanagement, habits, selfimprovement"),
]

random.seed(today.toordinal())
topic, tags = random.choice(TOPICS)

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"]

def groq(prompt, tokens=1200):
    for model in MODELS:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": tokens},
                timeout=30
            )
            resp = r.json()
            if "choices" in resp:
                return resp["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"⚠️ {model}: {e}")
    raise Exception("All Groq models failed")

print(f"🤖 Topic: {topic}")
guide       = groq(f"Write a detailed, practical guide titled '{topic}'. Use clear section headers with emojis. Be specific, honest, and conversational. Around 800 words.")
tagline     = groq(f"Write a single honest subtitle under 12 words for '{topic}'. No hype, no exclamation marks.", 60)
bullets_raw = groq(f"List exactly 5 things someone learns from '{topic}'. Each under 10 words. Plain lines only.", 200)
seo_desc    = groq(f"Write a natural meta description under 155 characters for '{topic}'.", 80)
devto_intro = groq(f"Write 3 short paragraphs introducing '{topic}'. Give genuine useful advice. End by mentioning a full guide at {GUIDE_URL}. Write like a person.", 400)
tumblr_post = groq(f"Write a short casual Tumblr post about '{topic}'. Two paragraphs. Sound like a real person. Link to {GUIDE_URL}. Finish with hashtags.", 300)

bullet_list = [b.strip("•-– \t*") for b in bullets_raw.strip().split("\n") if b.strip()][:5]

def md_to_html(text):
    lines, out = text.split("\n"), []
    for line in lines:
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        if re.match(r'^#{1,3} ', line):
            out.append(f"<h2>{line.lstrip('#').strip()}</h2>")
        elif line.strip():
            out.append(f"<p>{line}</p>")
    return "\n".join(out)

paragraphs   = [p for p in guide.split("\n") if p.strip()]
preview_html = md_to_html("\n".join(paragraphs[:5]))
locked_html  = md_to_html("\n".join(paragraphs[5:]))
full_html    = md_to_html("\n".join(paragraphs))
bullets_html = "\n".join(f'<li><span class="check">✓</span> {b}</li>' for b in bullet_list)

os.makedirs("docs/guides", exist_ok=True)

# ── Load / update guide index ─────────────────────────────────────────────────
index_file = "docs/guides/index.json"
all_guides = []
if os.path.exists(index_file):
    with open(index_file) as f:
        all_guides = json.load(f)
if not any(g["date"] == DATE_STR for g in all_guides):
    all_guides.insert(0, {"date": DATE_STR, "topic": topic,
                           "url": f"guides/{DATE_STR}.html", "tagline": tagline})
with open(index_file, "w") as f:
    json.dump(all_guides, f)

# ── Load blocklist ────────────────────────────────────────────────────────────
blocklist_file = "docs/blocklist.json"
blocklist = []
if os.path.exists(blocklist_file):
    with open(blocklist_file) as f:
        blocklist = json.load(f)

# ── Shared CSS ────────────────────────────────────────────────────────────────
SHARED_CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --ink: #1a1a2e; --ink-light: #4a4a6a; --accent: #2563eb;
    --accent-light: #eff6ff; --border: #e5e7eb; --bg: #fafaf8; --white: #ffffff;
    --green: #166534; --green-light: #f0fdf4; --green-border: #bbf7d0;
  }
  body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--ink); line-height: 1.75; }
  .topbar {
    background: var(--white); border-bottom: 1px solid var(--border);
    padding: 14px 24px; display: flex; justify-content: space-between;
    align-items: center; font-size: 0.82rem; color: var(--ink-light);
  }
  .topbar-logo { font-family: 'Lora', serif; font-weight: 700; font-size: 1rem; color: var(--ink); text-decoration: none; }
  footer {
    text-align: center; padding: 40px 24px; font-size: 0.78rem;
    color: var(--ink-light); border-top: 1px solid var(--border); background: var(--white);
  }
  footer a { color: var(--ink-light); text-decoration: underline; }
  .footer-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 12px; flex-wrap: wrap; }
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>'

def page_footer():
    return f"""<footer>
  <div class="footer-links">
    <a href="/auto-income-bot/">All guides</a>
    <a href="/auto-income-bot/legal.html">Privacy & Terms</a>
    <a href="/auto-income-bot/contact.html">Contact</a>
  </div>
  <p>© {today.year} Daily Guides · New guide every day</p>
  <p style="margin-top:6px;font-size:0.72rem;color:#9ca3af">Guides are informational only and do not constitute professional advice.</p>
</footer>"""

# ── GUIDE PAGE (buyers) ───────────────────────────────────────────────────────
guide_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="robots" content="noindex, nofollow"/>
  <title>{topic} — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .access-bar {{
      background: var(--green-light); border-bottom: 1px solid var(--green-border);
      padding: 12px 24px; text-align: center; font-size: 0.85rem;
      color: var(--green); font-weight: 500;
    }}
    .article {{ max-width: 680px; margin: 0 auto; padding: 60px 24px 80px; }}
    .article-label {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 16px; }}
    .article h1 {{ font-family: 'Lora', serif; font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 700; line-height: 1.2; margin-bottom: 24px; letter-spacing: -0.02em; }}
    .article-meta {{ display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.8rem; color: #6b7280; margin-bottom: 40px; padding-bottom: 32px; border-bottom: 1px solid var(--border); }}
    .article-body {{ font-family: 'Lora', serif; font-size: 1.05rem; color: #2d2d4e; line-height: 1.9; }}
    .article-body h2 {{ font-family: 'Lora', serif; font-size: 1.3rem; font-weight: 700; color: var(--ink); margin: 40px 0 14px; }}
    .article-body p {{ margin-bottom: 20px; }}
    .save-box {{
      margin-top: 48px; padding: 28px 32px; background: var(--white);
      border: 1px solid var(--border); border-radius: 12px;
    }}
    .save-box h3 {{ font-size: 1rem; font-weight: 600; margin-bottom: 10px; }}
    .save-box p {{ font-size: 0.88rem; color: #6b7280; margin-bottom: 16px; line-height: 1.6; }}
    .save-url {{ background: #f3f4f6; border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px; font-size: 0.78rem; color: #374151; word-break: break-all; font-family: monospace; margin-bottom: 12px; }}
    .copy-btn {{ display: inline-block; background: var(--accent); color: white; padding: 10px 20px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; border: none; cursor: pointer; }}
    .copy-btn:hover {{ background: #1d4ed8; }}
    .sub-upsell {{ margin-top: 16px; padding: 16px; background: var(--accent-light); border-radius: 8px; font-size: 0.85rem; color: #1e40af; }}
    .sub-upsell a {{ color: #1e40af; font-weight: 600; }}
    @media(max-width:600px) {{ .article {{ padding: 40px 20px 60px; }} .save-box {{ padding: 20px; }} }}
  </style>
  <script>
    window.onload = function() {{
      var params = new URLSearchParams(window.location.search);
      if (params.get('key') !== '{GUIDE_KEY}') {{
        window.location.href = '/auto-income-bot/';
      }}
      document.getElementById('page-url').textContent = window.location.href;
    }};
    function copyLink() {{
      navigator.clipboard.writeText(window.location.href).then(function() {{
        var btn = document.getElementById('copy-btn');
        btn.textContent = '✓ Copied!';
        setTimeout(function() {{ btn.textContent = 'Copy link'; }}, 2000);
      }});
    }}
  </script>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
  <a href="/auto-income-bot/" style="color:var(--ink-light);text-decoration:none;font-size:0.82rem">← All guides</a>
</div>
<div class="access-bar">✓ Purchase confirmed — you have permanent access to this guide.</div>
<div class="article">
  <div class="article-label">Full Guide — {today.strftime('%B %d, %Y')}</div>
  <h1>{topic}</h1>
  <div class="article-meta">
    <span>📄 Full guide</span>
    <span>⏱ ~5 min read</span>
    <span>🔒 Purchased {today.strftime('%B %d, %Y')}</span>
  </div>
  <div class="article-body">{full_html}</div>
  <div class="save-box">
    <h3>💾 Save your guide link</h3>
    <p>This link is yours permanently. Copy it into your notes or email it to yourself.</p>
    <div class="save-url" id="page-url">Loading...</div>
    <button class="copy-btn" id="copy-btn" onclick="copyLink()">Copy link</button>
    <div class="sub-upsell">
      📚 Want access to <strong>every guide</strong>, past and future?
      <a href="{STRIPE_SUB_URL}">Subscribe for $6.99/month →</a>
    </div>
  </div>
</div>
{page_footer()}
</body>
</html>"""

# ── ARCHIVE PAGE (subscribers only) ──────────────────────────────────────────
def build_archive():
    cards = ""
    for g in all_guides:
        cards += f"""<a class="guide-card" href="/auto-income-bot/{g['url']}?key={GUIDE_KEY}">
      <div class="card-date">{datetime.datetime.strptime(g['date'],'%Y-%m-%d').strftime('%B %d, %Y')}</div>
      <div class="card-title">{g['topic']}</div>
      <div class="card-tagline">{g.get('tagline','')}</div>
      <span class="card-cta">Read guide →</span>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="robots" content="noindex, nofollow"/>
  <title>Full Archive — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .access-bar {{ background: var(--green-light); border-bottom: 1px solid var(--green-border); padding: 12px 24px; text-align: center; font-size: 0.85rem; color: var(--green); font-weight: 500; }}
    .wrap {{ max-width: 780px; margin: 0 auto; padding: 48px 24px; }}
    .wrap h1 {{ font-family: 'Lora', serif; font-size: clamp(1.6rem,3vw,2.2rem); font-weight: 700; margin-bottom: 8px; }}
    .wrap .sub {{ color: var(--ink-light); font-size: 0.95rem; margin-bottom: 32px; }}
    .guides-grid {{ display: flex; flex-direction: column; gap: 14px; }}
    .guide-card {{ display: block; background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 22px 26px; text-decoration: none; color: inherit; transition: border-color 0.2s, box-shadow 0.2s; }}
    .guide-card:hover {{ border-color: var(--accent); box-shadow: 0 4px 16px rgba(37,99,235,0.08); }}
    .card-date {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin-bottom: 5px; }}
    .card-title {{ font-family: 'Lora', serif; font-size: 1.1rem; font-weight: 700; color: var(--ink); margin-bottom: 5px; line-height: 1.3; }}
    .card-tagline {{ font-size: 0.85rem; color: var(--ink-light); margin-bottom: 12px; }}
    .card-cta {{ font-size: 0.8rem; font-weight: 600; color: var(--accent); }}
    @media(max-width:600px) {{ .wrap {{ padding: 32px 16px; }} }}
  </style>
  <script>
    window.onload = function() {{
      var params = new URLSearchParams(window.location.search);
      var subCode = params.get('sub');
      if (!subCode || subCode.length < 8) {{
        window.location.href = '/auto-income-bot/';
        return;
      }}
      // Check blocklist
      fetch('/auto-income-bot/blocklist.json')
        .then(r => r.json())
        .then(function(blocked) {{
          if (blocked.includes(subCode)) {{
            document.getElementById('content').innerHTML = '<div style="text-align:center;padding:60px 24px"><h2>Access revoked</h2><p style="margin-top:12px;color:#6b7280">Your subscription has been cancelled. <a href="{STRIPE_SUB_URL}">Resubscribe here</a>.</p></div>';
          }}
        }}).catch(function() {{}});
    }};
  </script>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
  <span style="font-size:0.82rem;color:var(--green);font-weight:500">✓ Subscriber access</span>
</div>
<div class="access-bar">✓ Subscriber — you have access to all {len(all_guides)} guides</div>
<div class="wrap" id="content">
  <h1>Full Guide Archive</h1>
  <p class="sub">{len(all_guides)} guides available · New one added every day</p>
  <div class="guides-grid">{cards}</div>
</div>
{page_footer()}
</body>
</html>"""

# ── HOMEPAGE (public, shows all guides with buy buttons) ──────────────────────
def build_homepage():
    cards = ""
    for g in all_guides:
        is_today = g["date"] == DATE_STR
        badge = '<span style="background:#2563eb;color:white;font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:999px;margin-left:8px;vertical-align:middle">NEW</span>' if is_today else ""
        cards += f"""<div class="guide-card">
      <div class="card-date">{datetime.datetime.strptime(g['date'],'%Y-%m-%d').strftime('%B %d, %Y')}{badge}</div>
      <div class="card-title">{g['topic']}</div>
      <div class="card-tagline">{g.get('tagline','')}</div>
      <a class="card-btn" href="/auto-income-bot/{g['url']}">Preview & buy — $1.99 →</a>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="Daily practical guides on money, health, productivity and more. New guide every day from $1.99."/>
  <title>Daily Guides — Practical guides on everyday life</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .hero {{ background: var(--white); border-bottom: 1px solid var(--border); padding: 64px 24px 56px; text-align: center; }}
    .hero h1 {{ font-family: 'Lora', serif; font-size: clamp(1.8rem,4vw,2.8rem); font-weight: 700; line-height: 1.2; margin-bottom: 14px; letter-spacing: -0.02em; }}
    .hero p {{ font-size: 1rem; color: var(--ink-light); max-width: 480px; margin: 0 auto 32px; }}
    .sub-banner {{
      display: inline-flex; align-items: center; gap: 12px; flex-wrap: wrap; justify-content: center;
      background: var(--accent-light); border: 1px solid #bfdbfe; border-radius: 10px;
      padding: 14px 24px; font-size: 0.88rem; color: #1e40af;
    }}
    .sub-banner a {{ background: var(--accent); color: white; padding: 8px 18px; border-radius: 6px; font-weight: 600; text-decoration: none; font-size: 0.85rem; }}
    .sub-banner a:hover {{ background: #1d4ed8; }}
    .wrap {{ max-width: 780px; margin: 0 auto; padding: 48px 24px; }}
    .wrap h2 {{ font-family: 'Lora', serif; font-size: 1.2rem; font-weight: 700; margin-bottom: 24px; }}
    .guides-grid {{ display: flex; flex-direction: column; gap: 16px; }}
    .guide-card {{ background: var(--white); border: 1px solid var(--border); border-radius: 10px; padding: 24px 28px; }}
    .card-date {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); margin-bottom: 6px; }}
    .card-title {{ font-family: 'Lora', serif; font-size: 1.1rem; font-weight: 700; color: var(--ink); margin-bottom: 5px; line-height: 1.3; }}
    .card-tagline {{ font-size: 0.85rem; color: var(--ink-light); margin-bottom: 14px; }}
    .card-btn {{ display: inline-block; background: var(--accent); color: white; padding: 9px 18px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; text-decoration: none; }}
    .card-btn:hover {{ background: #1d4ed8; }}
    @media(max-width:600px) {{ .wrap {{ padding: 32px 16px; }} .guide-card {{ padding: 18px 20px; }} }}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
  <span>New guide every day</span>
</div>
<div class="hero">
  <h1>Practical guides for everyday life.</h1>
  <p>Clear, honest guides on money, health, productivity and more. New topic every day.</p>
  <div class="sub-banner">
    📚 <span>Want access to <strong>all guides</strong>, every day?</span>
    <a href="{STRIPE_SUB_URL}">Subscribe — $6.99/month →</a>
  </div>
</div>
<div class="wrap">
  <h2>All guides ({len(all_guides)} available)</h2>
  <div class="guides-grid">{cards}</div>
</div>
{page_footer()}
</body>
</html>"""

# ── SALES PAGE (individual guide preview + buy) ───────────────────────────────
sales_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{seo_desc}"/>
  <meta property="og:title" content="{topic}"/>
  <meta property="og:description" content="{seo_desc}"/>
  <title>{topic} — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .hero {{ background: var(--white); border-bottom: 1px solid var(--border); padding: 72px 24px 64px; text-align: center; }}
    .hero-inner {{ max-width: 680px; margin: 0 auto; }}
    .category-tag {{ display: inline-block; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 20px; }}
    .hero h1 {{ font-family: 'Lora', serif; font-size: clamp(1.9rem,4vw,3rem); font-weight: 700; line-height: 1.2; margin-bottom: 16px; letter-spacing: -0.02em; }}
    .hero-tagline {{ font-size: 1.05rem; color: var(--ink-light); max-width: 520px; margin: 0 auto 36px; }}
    .hero-meta {{ font-size: 0.8rem; color: var(--ink-light); margin-bottom: 32px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
    .pricing-row {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 14px; }}
    .btn-single {{ display: inline-block; background: var(--accent); color: white; padding: 15px 32px; border-radius: 8px; font-size: 0.95rem; font-weight: 600; text-decoration: none; transition: background 0.2s, transform 0.2s; }}
    .btn-single:hover {{ background: #1d4ed8; transform: translateY(-2px); }}
    .btn-sub {{ display: inline-block; background: var(--white); color: var(--accent); border: 2px solid var(--accent); padding: 13px 32px; border-radius: 8px; font-size: 0.95rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }}
    .btn-sub:hover {{ background: var(--accent-light); transform: translateY(-2px); }}
    .pricing-note {{ font-size: 0.75rem; color: var(--ink-light); margin-top: 4px; }}
    .section {{ max-width: 680px; margin: 0 auto; padding: 56px 24px; }}
    .section + .section {{ border-top: 1px solid var(--border); }}
    .section-label {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }}
    .section h2 {{ font-family: 'Lora', serif; font-size: clamp(1.4rem,2.5vw,1.9rem); font-weight: 700; line-height: 1.25; margin-bottom: 28px; }}
    .learn-list {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
    .learn-list li {{ display: flex; align-items: flex-start; gap: 12px; font-size: 0.97rem; padding: 14px 18px; background: var(--accent-light); border-radius: 8px; border-left: 3px solid var(--accent); }}
    .check {{ color: var(--accent); font-weight: 700; flex-shrink: 0; }}
    .preview-content {{ font-family: 'Lora', serif; font-size: 1.02rem; color: #2d2d4e; line-height: 1.85; }}
    .preview-content h2 {{ font-size: 1.15rem; font-weight: 600; margin: 24px 0 10px; font-family: 'Lora', serif; }}
    .preview-content p {{ margin-bottom: 16px; }}
    .blur-zone {{ position: relative; margin-top: 8px; }}
    .blurred {{ filter: blur(5px); user-select: none; pointer-events: none; opacity: 0.55; max-height: 140px; overflow: hidden; font-family: 'Lora', serif; line-height: 1.85; }}
    .blur-fade {{ position: absolute; bottom: 0; left: 0; right: 0; height: 90px; background: linear-gradient(transparent, var(--bg)); }}
    .paywall-note {{ text-align: center; margin-top: 24px; padding: 20px; background: var(--white); border: 1px solid var(--border); border-radius: 8px; font-size: 0.9rem; color: var(--ink-light); }}
    .cta-section {{ background: var(--ink); color: white; padding: 56px 24px; text-align: center; }}
    .cta-inner {{ max-width: 560px; margin: 0 auto; }}
    .cta-section h2 {{ font-family: 'Lora', serif; font-size: clamp(1.5rem,3vw,2.1rem); font-weight: 700; margin-bottom: 12px; }}
    .cta-section p {{ color: rgba(255,255,255,0.65); font-size: 0.95rem; margin-bottom: 32px; }}
    .cta-pricing {{ display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 12px; }}
    .btn-cta-single {{ display: inline-block; background: white; color: var(--ink); padding: 16px 36px; border-radius: 8px; font-size: 0.95rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }}
    .btn-cta-single:hover {{ background: #f0f0f0; transform: translateY(-2px); }}
    .btn-cta-sub {{ display: inline-block; background: transparent; color: white; border: 2px solid rgba(255,255,255,0.4); padding: 14px 36px; border-radius: 8px; font-size: 0.95rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }}
    .btn-cta-sub:hover {{ border-color: white; transform: translateY(-2px); }}
    .cta-guarantee {{ margin-top: 16px; font-size: 0.78rem; color: rgba(255,255,255,0.4); }}
    .notice {{ background: #fffbeb; border-top: 1px solid #fde68a; border-bottom: 1px solid #fde68a; text-align: center; padding: 12px 24px; font-size: 0.83rem; color: #92400e; font-weight: 500; }}
    @media(max-width:600px) {{ .hero {{ padding: 48px 20px 40px; }} .section {{ padding: 40px 20px; }} .cta-section {{ padding: 48px 20px; }} .pricing-row, .cta-pricing {{ flex-direction: column; align-items: center; }} }}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
  <span style="font-size:0.82rem">New guide every day</span>
</div>
<div class="hero">
  <div class="hero-inner">
    <div class="category-tag">📖 {today.strftime('%B %d, %Y')}</div>
    <h1>{topic}</h1>
    <p class="hero-tagline">{tagline}</p>
    <div class="hero-meta">
      <span>📄 ~800 words</span>
      <span>⏱ 5 min read</span>
      <span>✓ Permanent access</span>
    </div>
    <div class="pricing-row">
      <a href="{STRIPE_SINGLE_URL}" class="btn-single">This guide — $1.99 →</a>
      <a href="{STRIPE_SUB_URL}" class="btn-sub">All guides — $6.99/mo →</a>
    </div>
    <p class="pricing-note">One-time payment · or subscribe for unlimited access · No hidden fees</p>
  </div>
</div>
<div class="section">
  <div class="section-label">Inside this guide</div>
  <h2>What you'll walk away with</h2>
  <ul class="learn-list">{bullets_html}</ul>
</div>
<div class="section">
  <div class="section-label">Free preview</div>
  <h2>Read the first section</h2>
  <div class="preview-content">{preview_html}</div>
  <div class="blur-zone">
    <div class="blurred preview-content">{locked_html[:700]}</div>
    <div class="blur-fade"></div>
  </div>
  <div class="paywall-note"><strong>End of free preview.</strong> The full guide continues with practical steps you can use today.</div>
</div>
<div class="cta-section">
  <div class="cta-inner">
    <h2>Get the complete guide</h2>
    <p>Clear, practical, no fluff. Choose what works for you.</p>
    <div class="cta-pricing">
      <a href="{STRIPE_SINGLE_URL}" class="btn-cta-single">This guide — $1.99</a>
      <a href="{STRIPE_SUB_URL}" class="btn-cta-sub">All guides — $6.99/mo</a>
    </div>
    <p class="cta-guarantee">Secure payment via Stripe · 14-day refund if unsatisfied</p>
  </div>
</div>
<div class="notice">📅 A new guide publishes every day — each one stays available permanently after purchase.</div>
{page_footer()}
</body>
</html>"""

# ── REDIRECT PAGE ─────────────────────────────────────────────────────────────
redirect_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="robots" content="noindex"/>
  <title>Opening your guide...</title>
  <style>
    body {{ font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: #fafaf8; }}
    .box {{ text-align: center; padding: 40px; }}
    .spinner {{ width: 32px; height: 32px; border: 3px solid #e5e7eb; border-top-color: #2563eb; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    p {{ color: #6b7280; font-size: 0.9rem; margin-top: 8px; }}
  </style>
  <script>
    window.onload = function() {{
      var params = new URLSearchParams(window.location.search);
      if (params.get('key') !== '{GUIDE_KEY}') {{
        window.location.href = '/auto-income-bot/';
      }} else {{
        window.location.href = '/auto-income-bot/guides/{DATE_STR}.html?key={GUIDE_KEY}';
      }}
    }};
  </script>
</head>
<body>
  <div class="box">
    <div class="spinner"></div>
    <strong>Opening your guide...</strong>
    <p>You'll be redirected in a moment.</p>
  </div>
</body>
</html>"""

# ── SUBSCRIBER REDIRECT (Stripe sends here, generates their unique code) ──────
sub_redirect = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="robots" content="noindex"/>
  <title>Setting up your access...</title>
  <style>
    body {{ font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: #fafaf8; }}
    .box {{ text-align: center; padding: 40px; max-width: 480px; }}
    .spinner {{ width: 32px; height: 32px; border: 3px solid #e5e7eb; border-top-color: #2563eb; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    h2 {{ font-size: 1.3rem; margin-bottom: 10px; color: #1a1a2e; }}
    p {{ color: #6b7280; font-size: 0.88rem; line-height: 1.6; margin-bottom: 16px; }}
    .archive-link {{ display: inline-block; background: #2563eb; color: white; padding: 12px 28px; border-radius: 8px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
    .save-url {{ background: #f3f4f6; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px 14px; font-size: 0.78rem; color: #374151; word-break: break-all; font-family: monospace; margin: 12px 0; text-align: left; }}
    .copy-btn {{ background: #e5e7eb; border: none; padding: 8px 16px; border-radius: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; margin-bottom: 16px; }}
    #loading {{ display: block; }}
    #content {{ display: none; }}
  </style>
  <script>
    // Simple hash function (same logic as Python's make_sub_code)
    async function makeSubCode(email) {{
      const salt = '{SUB_SALT}';
      const data = salt + email.toLowerCase().trim();
      const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(data));
      const arr = Array.from(new Uint8Array(buf));
      return arr.map(b => b.toString(16).padStart(2,'0')).join('').slice(0,12);
    }}

    window.onload = async function() {{
      // Get email from Stripe URL param if present, otherwise prompt
      var params = new URLSearchParams(window.location.search);
      var email = params.get('prefilled_email') || params.get('customer_email') || '';

      if (!email) {{
        email = prompt('Please enter the email address you used to subscribe:') || '';
      }}

      if (!email) {{
        window.location.href = '/auto-income-bot/';
        return;
      }}

      var code = await makeSubCode(email);

      // Check blocklist
      try {{
        var r = await fetch('/auto-income-bot/blocklist.json');
        var blocked = await r.json();
        if (blocked.includes(code)) {{
          document.getElementById('loading').style.display = 'none';
          document.getElementById('content').innerHTML = '<h2>Access revoked</h2><p>Your subscription has been cancelled. <a href="{STRIPE_SUB_URL}">Resubscribe here →</a></p>';
          document.getElementById('content').style.display = 'block';
          return;
        }}
      }} catch(e) {{}}

      var archiveUrl = '/auto-income-bot/archive.html?sub=' + code;
      document.getElementById('loading').style.display = 'none';
      document.getElementById('archive-link').href = archiveUrl;
      document.getElementById('save-url').textContent = window.location.origin + archiveUrl;
      document.getElementById('content').style.display = 'block';
    }};

    function copyLink() {{
      var url = window.location.origin + document.getElementById('archive-link').getAttribute('href');
      navigator.clipboard.writeText(url).then(function() {{
        var btn = document.getElementById('copy-btn');
        btn.textContent = '✓ Copied!';
        setTimeout(function() {{ btn.textContent = 'Copy my link'; }}, 2000);
      }});
    }}
  </script>
</head>
<body>
  <div class="box">
    <div id="loading">
      <div class="spinner"></div>
      <strong>Setting up your access...</strong>
    </div>
    <div id="content">
      <h2>✓ Subscription active!</h2>
      <p>Your personal archive link is ready. Save it somewhere safe — it's yours as long as your subscription is active.</p>
      <div class="save-url" id="save-url"></div>
      <button class="copy-btn" id="copy-btn" onclick="copyLink()">Copy my link</button>
      <br>
      <a class="archive-link" id="archive-link" href="#">Open full archive →</a>
      <p style="margin-top:16px;font-size:0.78rem;color:#9ca3af">Tip: email this link to yourself so you never lose it.</p>
    </div>
  </div>
</body>
</html>"""

# ── CONTACT PAGE ──────────────────────────────────────────────────────────────
contact_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Contact — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .wrap {{ max-width: 560px; margin: 0 auto; padding: 60px 24px; }}
    h1 {{ font-family: 'Lora', serif; font-size: 1.8rem; font-weight: 700; margin-bottom: 10px; }}
    p {{ color: var(--ink-light); margin-bottom: 28px; font-size: 0.95rem; }}
    .form-group {{ margin-bottom: 20px; }}
    label {{ display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 6px; color: var(--ink); }}
    input, textarea {{ width: 100%; padding: 12px 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 0.95rem; font-family: 'Inter', sans-serif; background: var(--white); color: var(--ink); transition: border-color 0.2s; }}
    input:focus, textarea:focus {{ outline: none; border-color: var(--accent); }}
    textarea {{ height: 140px; resize: vertical; }}
    .submit-btn {{ background: var(--accent); color: white; padding: 14px 32px; border: none; border-radius: 8px; font-size: 0.95rem; font-weight: 600; cursor: pointer; width: 100%; transition: background 0.2s; }}
    .submit-btn:hover {{ background: #1d4ed8; }}
    .back {{ display: inline-block; margin-bottom: 32px; font-size: 0.85rem; color: var(--accent); text-decoration: none; }}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
</div>
<div class="wrap">
  <a href="/auto-income-bot/" class="back">← Back</a>
  <h1>Contact us</h1>
  <p>Questions about a purchase, refund requests, or anything else — we'll get back to you within 48 hours.</p>
  <form action="https://formspree.io/f/{FORMSPREE_ID}" method="POST">
    <div class="form-group">
      <label for="email">Your email address</label>
      <input type="email" id="email" name="email" placeholder="you@example.com" required/>
    </div>
    <div class="form-group">
      <label for="subject">Subject</label>
      <input type="text" id="subject" name="subject" placeholder="e.g. Refund request, question about my guide..." required/>
    </div>
    <div class="form-group">
      <label for="message">Message</label>
      <textarea id="message" name="message" placeholder="Tell us what you need..." required></textarea>
    </div>
    <button type="submit" class="submit-btn">Send message →</button>
  </form>
</div>
{page_footer()}
</body>
</html>"""

# ── LEGAL PAGE ────────────────────────────────────────────────────────────────
legal_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Privacy Policy & Terms — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .wrap {{ max-width: 680px; margin: 0 auto; padding: 60px 24px; }}
    h1 {{ font-family: 'Lora', serif; font-size: 2rem; margin-bottom: 8px; }}
    h2 {{ font-family: 'Lora', serif; font-size: 1.2rem; margin: 36px 0 10px; }}
    p {{ margin-bottom: 14px; color: #374151; }}
    a {{ color: var(--accent); }}
    .back {{ display: inline-block; margin-bottom: 32px; font-size: 0.85rem; color: var(--accent); text-decoration: none; }}
    .updated {{ font-size: 0.8rem; color: #9ca3af; margin-bottom: 40px; }}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
</div>
<div class="wrap">
  <a href="/auto-income-bot/" class="back">← Back</a>
  <h1>Privacy Policy & Terms</h1>
  <p class="updated">Last updated: {today.strftime('%B %d, %Y')} · Operated from Switzerland</p>
  <h2>Who we are</h2>
  <p>Daily Guides is an independent digital publishing project operated by a private individual based in Switzerland. For any enquiries, use the <a href="/auto-income-bot/contact.html">contact form</a>.</p>
  <h2>What we sell</h2>
  <p>We sell digital guides delivered via permanent web access immediately after purchase. All content is informational and educational only. Nothing on this site constitutes professional financial, medical, legal, or psychological advice.</p>
  <h2>Payments</h2>
  <p>All payments are processed securely by Stripe. We do not store your payment details. <a href="https://stripe.com/privacy" target="_blank">Stripe's privacy policy</a> applies to all transactions.</p>
  <h2>Access to purchased content</h2>
  <p>After a one-time purchase, you are redirected immediately to a permanent private guide URL. After subscribing, you receive a personal archive link valid for the duration of your subscription. We recommend saving your link in your notes or emailing it to yourself.</p>
  <h2>Subscriptions</h2>
  <p>Subscriptions are billed monthly at $6.99 and can be cancelled at any time via Stripe. Access continues until the end of the current billing period.</p>
  <h2>EU Right of Withdrawal</h2>
  <p>Under EU consumer law you have a 14-day right of withdrawal. By completing your purchase and accessing the content immediately, you expressly waive this right per Article 16(m) of Directive 2011/83/EU. If you have not accessed the content, contact us within 14 days for a full refund.</p>
  <h2>Refund Policy</h2>
  <p>If unsatisfied for any reason, contact us within 14 days via the <a href="/auto-income-bot/contact.html">contact form</a> for a full refund — no questions asked.</p>
  <h2>Data we collect</h2>
  <p>We do not directly collect or store personal data. Stripe collects payment information. Contact form submissions are processed by Formspree. We do not sell or share any data.</p>
  <h2>Cookies</h2>
  <p>This site uses no tracking cookies or analytics scripts.</p>
  <h2>Swiss law</h2>
  <p>This site is operated in compliance with Swiss law (DSG/nDSG). Income is declared as personal income in Switzerland as required by law.</p>
  <h2>Disclaimer</h2>
  <p>All guides are for informational purposes only. Individual results vary. Nothing constitutes professional advice of any kind. Always consult a qualified professional for important decisions.</p>
</div>
{page_footer()}
</body>
</html>"""

# ── 404 PAGE ──────────────────────────────────────────────────────────────────
page_404 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Page not found — Daily Guides</title>
  {FONTS}
  <style>
    {SHARED_CSS}
    .wrap {{ max-width: 480px; margin: 0 auto; padding: 100px 24px; text-align: center; }}
    h1 {{ font-family: 'Lora', serif; font-size: 2rem; margin-bottom: 12px; }}
    p {{ color: var(--ink-light); margin-bottom: 28px; }}
    a {{ display: inline-block; background: var(--accent); color: white; padding: 12px 28px; border-radius: 8px; font-weight: 600; text-decoration: none; }}
  </style>
</head>
<body>
<div class="topbar">
  <a href="/auto-income-bot/" class="topbar-logo">Daily Guides</a>
</div>
<div class="wrap">
  <h1>Page not found</h1>
  <p>The page you're looking for doesn't exist. Head back to the homepage to browse all available guides.</p>
  <a href="/auto-income-bot/">Back to Daily Guides →</a>
</div>
{page_footer()}
</body>
</html>"""

# ── SITEMAP ───────────────────────────────────────────────────────────────────
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>
  <url><loc>{SITE_URL}/legal.html</loc><changefreq>monthly</changefreq><priority>0.3</priority></url>
  <url><loc>{SITE_URL}/contact.html</loc><changefreq>monthly</changefreq><priority>0.3</priority></url>
</urlset>"""

# ── ROBOTS.TXT ────────────────────────────────────────────────────────────────
robots = f"""User-agent: *
Allow: /auto-income-bot/
Allow: /auto-income-bot/legal.html
Allow: /auto-income-bot/contact.html
Disallow: /auto-income-bot/guides/
Disallow: /auto-income-bot/archive.html
Disallow: /auto-income-bot/redirect.html
Disallow: /auto-income-bot/sub-redirect.html
Sitemap: {SITE_URL}/sitemap.xml"""

# ── Write all files ───────────────────────────────────────────────────────────
print("💾 Writing all pages...")
files = {
    "docs/index.html":         build_homepage(),
    "docs/today.html":         sales_html,
    f"docs/guides/{DATE_STR}.html": guide_page,
    "docs/archive.html":       build_archive(),
    "docs/redirect.html":      redirect_page,
    "docs/sub-redirect.html":  sub_redirect,
    "docs/contact.html":       contact_page,
    "docs/legal.html":         legal_html,
    "docs/404.html":           page_404,
    "docs/sitemap.xml":        sitemap,
    "docs/robots.txt":         robots,
}
if not os.path.exists(blocklist_file):
    with open(blocklist_file, "w") as f:
        json.dump([], f)

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
print("✅ All pages saved")

# ── POST TO DEV.TO ────────────────────────────────────────────────────────────
print("📝 Posting to Dev.to...")
try:
    tag_list = [t.strip().lower() for t in tags.split(",")][:4]
    devto_body = f"{devto_intro}\n\n---\n\n*Full guide: [{topic}]({GUIDE_URL})*"
    r = requests.post(
        "https://dev.to/api/articles",
        headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"},
        json={"article": {
            "title": topic, "body_markdown": devto_body,
            "published": True, "tags": tag_list, "canonical_url": GUIDE_URL
        }}
    )
    if r.status_code in [200, 201]:
        print(f"✅ Dev.to: {r.json().get('url', '')}")
    else:
        print(f"⚠️ Dev.to {r.status_code}: {r.text[:200]}")
except Exception as e:
    print(f"⚠️ Dev.to: {e}")

# ── POST TO TUMBLR ────────────────────────────────────────────────────────────
print("📝 Posting to Tumblr...")
try:
    auth = OAuth1(TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET,
                  TUMBLR_OAUTH_TOKEN, TUMBLR_OAUTH_SECRET)
    r = requests.post(
        f"https://api.tumblr.com/v2/blog/{TUMBLR_BLOG_NAME}.tumblr.com/post",
        auth=auth,
        json={"type": "text", "title": topic,
              "body": tumblr_post.replace("\n", "<br>"),
              "tags": [t.strip() for t in tags.split(",")]}
    )
    if r.status_code in [200, 201]:
        print("✅ Tumblr posted")
    else:
        print(f"⚠️ Tumblr {r.status_code}: {r.text[:200]}")
except Exception as e:
    print(f"⚠️ Tumblr: {e}")

print(f"\n🎉 All done for {today}! Topic: '{topic}'")
