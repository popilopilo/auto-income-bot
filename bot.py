import os, requests, datetime, re, random
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

STRIPE_URL   = "https://buy.stripe.com/bJeaEX4sUdDn0M99dF9fW00"
CONTACT_EMAIL = "laila.barriosm@gmail.com"

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
    ("How to Negotiate a Higher Salary (And Actually Win)", "career, money, finance, professionaldevelopment"),
    ("A Simple System for Keeping Your Home Clean", "organization, cleaning, homeimprovement, habits"),
    ("How to Build an Emergency Fund From Zero", "personalfinance, savings, money, budgeting"),
    ("The Beginner's Guide to Meditation (No App Required)", "meditation, wellness, mindfulness, selfimprovement"),
    ("How to Drink Less Without Feeling Left Out", "health, wellness, lifestyle, habits"),
    ("A Practical Guide to Better Posture at Your Desk", "health, fitness, workfromhome, wellness"),
    ("How to Save for a Holiday Without Going Broke", "travel, savings, personalfinance, budgeting"),
    ("The Simple Anti-Anxiety Toolkit That Actually Helps", "mentalhealth, wellness, anxiety, selfimprovement"),
    ("How to Learn Any Skill Twice as Fast", "learning, productivity, selfimprovement, skills"),
    ("A Guide to Eating Out Without Ruining Your Budget", "food, budgeting, personalfinance, lifestyle"),
    ("How to Finally Get Organised at Home", "organization, productivity, homeimprovement, habits"),
    ("The Beginner's Guide to Running (From Zero to 5K)", "running, fitness, health, exercise"),
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
    ("How to Get a Better Night's Sleep Tonight", "sleep, health, wellness, selfimprovement"),
    ("The Realistic Guide to Working Out With No Motivation", "fitness, exercise, habits, selfimprovement"),
    ("How to Spend Less Time on Social Media", "productivity, mentalhealth, habits, focus"),
    ("A Guide to Cooking Cheap, Delicious Meals Every Night", "food, budgeting, mealprep, cooking"),
    ("How to Set Goals You Actually Achieve", "selfimprovement, productivity, habits, goals"),
    ("The Beginner's Guide to Strength Training at Home", "fitness, exercise, health, hometraining"),
    ("How to Handle a Job Interview With Confidence", "career, confidence, professionaldevelopment, selfimprovement"),
    ("A Simple Plan for Getting Out of Your Comfort Zone", "selfimprovement, mindset, personaldevelopment, confidence"),
    ("How to Write Better Emails That Get Replies", "career, productivity, professionaldevelopment, writing"),
    ("The Lazy Person's Guide to Eating Healthier", "health, food, healthyeating, wellness"),
    ("How to Stop Worrying About Things You Can't Control", "mentalhealth, wellness, mindfulness, selfimprovement"),
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
    ("How to Cook Meal Prep That You'll Actually Eat", "mealprep, food, healthyeating, cooking"),
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
    ("How to Start Saving When You Think You Can't Afford To", "personalfinance, savings, budgeting, money"),
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

today = datetime.date.today()
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
            print(f"⚠️ Model {model} failed, trying next...")
        except Exception as e:
            print(f"⚠️ {model} error: {e}")
    raise Exception("All Groq models failed")

print(f"🤖 Topic: {topic}")
guide       = groq(f"Write a detailed, practical guide titled '{topic}'. Use clear section headers with emojis. Be specific, honest, and conversational. Around 800 words.")
tagline     = groq(f"Write a single honest subtitle under 12 words for '{topic}'. No hype, no exclamation marks.", 60)
bullets_raw = groq(f"List exactly 5 things someone learns from '{topic}'. Each under 10 words. Plain lines only.", 200)
seo_desc    = groq(f"Write a natural meta description under 155 characters for '{topic}'. Sound helpful, not salesy.", 80)
devto_intro = groq(f"Write 3 short paragraphs introducing '{topic}'. Give genuine useful advice. End by mentioning a full guide at {SITE_URL}. Write like a person.", 400)
tumblr_post = groq(f"Write a short casual Tumblr post about '{topic}'. Two paragraphs. Sound like a real person. Link to {SITE_URL}. Finish with a few hashtags.", 300)

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
bullets_html = "\n".join(f'<li><span class="check">✓</span> {b}</li>' for b in bullet_list)

# ── Privacy Policy & Terms (written once, stays permanent) ───────────────────
privacy_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Privacy Policy & Terms — Daily Guides</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:wght@700&display=swap" rel="stylesheet"/>
  <style>
    body {{ font-family: 'Inter', sans-serif; max-width: 680px; margin: 0 auto; padding: 60px 24px; color: #1a1a2e; line-height: 1.8; }}
    h1 {{ font-family: 'Lora', serif; font-size: 2rem; margin-bottom: 8px; }}
    h2 {{ font-family: 'Lora', serif; font-size: 1.2rem; margin: 36px 0 10px; }}
    p {{ margin-bottom: 14px; color: #374151; }}
    a {{ color: #2563eb; }}
    .back {{ display: inline-block; margin-bottom: 32px; font-size: 0.85rem; color: #2563eb; text-decoration: none; }}
    .updated {{ font-size: 0.8rem; color: #9ca3af; margin-bottom: 40px; }}
  </style>
</head>
<body>
  <a href="/" class="back">← Back to Daily Guides</a>
  <h1>Privacy Policy & Terms</h1>
  <p class="updated">Last updated: {today.strftime('%B %d, %Y')} · Operated from Switzerland</p>

  <h2>Who we are</h2>
  <p>Daily Guides is an independent publishing project operated by a private individual based in Switzerland. Contact: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>

  <h2>What we sell</h2>
  <p>We sell digital guides delivered via web access. Guides are informational and educational in nature. They do not constitute professional financial, medical, legal, or psychological advice.</p>

  <h2>Payments</h2>
  <p>All payments are processed securely by Stripe. We do not store your payment details. Stripe's privacy policy applies to all transactions: <a href="https://stripe.com/privacy" target="_blank">stripe.com/privacy</a></p>

  <h2>EU Right of Withdrawal</h2>
  <p>Under EU consumer law, you have a 14-day right of withdrawal for digital products. However, by completing your purchase and accessing the guide immediately, you expressly agree to waive this right in accordance with Article 16(m) of Directive 2011/83/EU. If you have not accessed the content, you may request a refund within 14 days by emailing <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>

  <h2>Refund Policy</h2>
  <p>If you are unsatisfied with your purchase for any reason, contact us within 14 days at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a> and we will issue a full refund — no questions asked.</p>

  <h2>Data we collect</h2>
  <p>We do not collect personal data directly. When you make a purchase, Stripe collects your payment information. We receive only your email address (if provided) to deliver your purchase. We do not sell, share, or use your data for marketing.</p>

  <h2>Cookies</h2>
  <p>This site does not use tracking cookies or analytics. No third-party advertising scripts are present.</p>

  <h2>Swiss law</h2>
  <p>This site is operated in compliance with Swiss law (DSG/nDSG). Income from this project is declared as personal income in Switzerland as required by law.</p>

  <h2>Disclaimer</h2>
  <p>All guides are for informational purposes only. Results vary by individual. Nothing on this site constitutes professional advice. Always consult a qualified professional for financial, medical, or legal decisions.</p>

  <h2>Contact</h2>
  <p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
</body>
</html>"""

# ── Main Landing Page HTML ────────────────────────────────────────────────────
print("🌐 Building landing page...")
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="description" content="{seo_desc}"/>
  <meta property="og:title" content="{topic}"/>
  <meta property="og:description" content="{seo_desc}"/>
  <title>{topic}</title>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --ink: #1a1a2e; --ink-light: #4a4a6a; --accent: #2563eb;
      --accent-light: #eff6ff; --border: #e5e7eb; --bg: #fafaf8; --white: #ffffff;
    }}
    body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--ink); line-height: 1.75; }}
    .topbar {{
      background: var(--white); border-bottom: 1px solid var(--border);
      padding: 14px 24px; display: flex; justify-content: space-between;
      align-items: center; font-size: 0.82rem; color: var(--ink-light);
    }}
    .topbar-logo {{ font-family: 'Lora', serif; font-weight: 700; font-size: 1rem; color: var(--ink); }}
    .hero {{
      background: var(--white); border-bottom: 1px solid var(--border);
      padding: 72px 24px 64px; text-align: center;
    }}
    .hero-inner {{ max-width: 680px; margin: 0 auto; }}
    .category-tag {{
      display: inline-block; font-size: 0.72rem; font-weight: 600;
      letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 20px;
    }}
    .hero h1 {{
      font-family: 'Lora', serif; font-size: clamp(1.9rem, 4vw, 3rem);
      font-weight: 700; line-height: 1.2; margin-bottom: 16px; letter-spacing: -0.02em;
    }}
    .hero-tagline {{ font-size: 1.05rem; color: var(--ink-light); max-width: 520px; margin: 0 auto 36px; }}
    .hero-meta {{
      font-size: 0.8rem; color: var(--ink-light); margin-bottom: 32px;
      display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;
    }}
    .hero-meta span {{ display: flex; align-items: center; gap: 5px; }}
    .btn-primary {{
      display: inline-block; background: var(--accent); color: white;
      padding: 16px 40px; border-radius: 8px; font-size: 1rem; font-weight: 600;
      text-decoration: none; transition: background 0.2s, transform 0.2s;
    }}
    .btn-primary:hover {{ background: #1d4ed8; transform: translateY(-2px); }}
    .hero-note {{ margin-top: 14px; font-size: 0.78rem; color: var(--ink-light); }}
    .section {{ max-width: 680px; margin: 0 auto; padding: 56px 24px; }}
    .section + .section {{ border-top: 1px solid var(--border); }}
    .section-label {{
      font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em;
      text-transform: uppercase; color: var(--accent); margin-bottom: 10px;
    }}
    .section h2 {{
      font-family: 'Lora', serif; font-size: clamp(1.4rem, 2.5vw, 1.9rem);
      font-weight: 700; line-height: 1.25; margin-bottom: 28px; letter-spacing: -0.02em;
    }}
    .learn-list {{ list-style: none; display: flex; flex-direction: column; gap: 14px; }}
    .learn-list li {{
      display: flex; align-items: flex-start; gap: 12px; font-size: 0.97rem;
      padding: 14px 18px; background: var(--accent-light); border-radius: 8px;
      border-left: 3px solid var(--accent);
    }}
    .check {{ color: var(--accent); font-weight: 700; flex-shrink: 0; margin-top: 1px; }}
    .preview-content {{ font-family: 'Lora', serif; font-size: 1.02rem; color: #2d2d4e; line-height: 1.85; }}
    .preview-content h2 {{ font-size: 1.15rem; font-weight: 600; color: var(--ink); margin: 24px 0 10px; font-family: 'Lora', serif; }}
    .preview-content p {{ margin-bottom: 16px; }}
    .blur-zone {{ position: relative; margin-top: 8px; }}
    .blurred {{ filter: blur(5px); user-select: none; pointer-events: none; opacity: 0.55; max-height: 140px; overflow: hidden; font-family: 'Lora', serif; font-size: 1.02rem; line-height: 1.85; }}
    .blur-fade {{ position: absolute; bottom: 0; left: 0; right: 0; height: 90px; background: linear-gradient(transparent, var(--bg)); }}
    .paywall-note {{
      text-align: center; margin-top: 24px; padding: 20px;
      background: var(--white); border: 1px solid var(--border); border-radius: 8px;
      font-size: 0.9rem; color: var(--ink-light);
    }}
    .cta-section {{ background: var(--ink); color: white; padding: 56px 24px; text-align: center; }}
    .cta-inner {{ max-width: 560px; margin: 0 auto; }}
    .cta-section h2 {{
      font-family: 'Lora', serif; font-size: clamp(1.5rem, 3vw, 2.1rem);
      font-weight: 700; line-height: 1.2; margin-bottom: 12px;
    }}
    .cta-section p {{ color: rgba(255,255,255,0.65); font-size: 0.95rem; margin-bottom: 32px; }}
    .price-row {{ display: flex; align-items: baseline; justify-content: center; gap: 8px; margin-bottom: 28px; }}
    .price-amount {{ font-size: 2.8rem; font-weight: 700; color: white; line-height: 1; }}
    .price-desc {{ font-size: 0.85rem; color: rgba(255,255,255,0.5); }}
    .btn-cta {{
      display: inline-block; background: white; color: var(--ink);
      padding: 17px 44px; border-radius: 8px; font-size: 1rem; font-weight: 600;
      text-decoration: none; transition: all 0.2s; width: 100%; max-width: 380px;
    }}
    .btn-cta:hover {{ background: #f0f0f0; transform: translateY(-2px); }}
    .cta-guarantee {{ margin-top: 16px; font-size: 0.78rem; color: rgba(255,255,255,0.45); }}
    .notice {{
      background: #fffbeb; border-top: 1px solid #fde68a; border-bottom: 1px solid #fde68a;
      text-align: center; padding: 12px 24px; font-size: 0.83rem; color: #92400e; font-weight: 500;
    }}
    footer {{
      text-align: center; padding: 40px 24px; font-size: 0.78rem;
      color: var(--ink-light); border-top: 1px solid var(--border); background: var(--white);
    }}
    footer a {{ color: var(--ink-light); text-decoration: underline; }}
    .footer-links {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 12px; }}
    @media(max-width:600px) {{
      .hero {{ padding: 48px 20px 40px; }}
      .section {{ padding: 40px 20px; }}
      .cta-section {{ padding: 48px 20px; }}
    }}
  </style>
</head>
<body>

<div class="topbar">
  <span class="topbar-logo">Daily Guides</span>
  <span>New guide every day</span>
</div>

<div class="hero">
  <div class="hero-inner">
    <div class="category-tag">📖 Today's Guide — {today.strftime('%B %d, %Y')}</div>
    <h1>{topic}</h1>
    <p class="hero-tagline">{tagline}</p>
    <div class="hero-meta">
      <span>📄 ~800 words</span>
      <span>⏱ 5 min read</span>
      <span>✓ Practical & actionable</span>
    </div>
    <a href="{STRIPE_URL}" class="btn-primary">Read the full guide — $4.99</a>
    <p class="hero-note">One-time payment · Instant access · No subscription</p>
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
  <div class="paywall-note">
    <strong>End of free preview.</strong> The full guide continues with practical steps you can use today.
  </div>
</div>

<div class="cta-section">
  <div class="cta-inner">
    <h2>Get the complete guide</h2>
    <p>Everything laid out clearly and practically. No fluff — just the stuff that works.</p>
    <div class="price-row">
      <span class="price-amount">$4.99</span>
      <span class="price-desc">one-time</span>
    </div>
    <a href="{STRIPE_URL}" class="btn-cta">Get instant access →</a>
    <p class="cta-guarantee">Secure payment via Stripe · 14-day refund if unsatisfied</p>
  </div>
</div>

<div class="notice">
  📅 A new guide publishes tomorrow — today's topic won't be here forever.
</div>

<footer>
  <div class="footer-links">
    <a href="/auto-income-bot/">Home</a>
    <a href="/auto-income-bot/legal.html">Privacy Policy & Terms</a>
    <a href="mailto:{CONTACT_EMAIL}">Contact</a>
  </div>
  <p>© {today.year} Daily Guides · Independent publishing project · Switzerland</p>
  <p style="margin-top:6px;font-size:0.72rem;color:#9ca3af">Guides are for informational purposes only and do not constitute professional advice.</p>
</footer>

</body>
</html>"""

os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("docs/legal.html", "w", encoding="utf-8") as f:
    f.write(privacy_html)
print("✅ Landing page + legal page saved")

# ── POST TO DEV.TO ────────────────────────────────────────────────────────────
print("📝 Posting to Dev.to...")
try:
    tag_list = [t.strip().lower() for t in tags.split(",")][:4]
    devto_body = f"{devto_intro}\n\n---\n\n*Full guide: [{topic}]({SITE_URL})*"
    r = requests.post(
        "https://dev.to/api/articles",
        headers={"api-key": DEVTO_API_KEY, "Content-Type": "application/json"},
        json={"article": {
            "title": topic, "body_markdown": devto_body,
            "published": True, "tags": tag_list, "canonical_url": SITE_URL
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

print(f"\n🎉 Done for {today}! Topic: '{topic}'")
