import os, requests, datetime, json

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_PRICE_ID = os.environ["STRIPE_PRICE_ID"]

topics = [
    "10 ways to save money on groceries",
    "Beginner guide to better sleep",
    "How to be more productive working from home",
    "Simple exercises you can do in 10 minutes",
    "Easy meals to prep for the whole week",
]

today = datetime.date.today()
topic = topics[today.toordinal() % len(topics)]

headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
payload = {
    "model": "llama3-8b-8192",
    "messages": [{"role": "user", "content": f"Write a detailed, helpful guide titled: '{topic}'. Make it practical, well-structured, and about 500 words."}]
}
r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
content = r.json()["choices"][0]["message"]["content"]

stripe_link = requests.post(
    "https://api.stripe.com/v1/payment_links",
    auth=(STRIPE_SECRET_KEY, ""),
    data={"line_items[0][price]": STRIPE_PRICE_ID, "line_items[0][quantity]": 1}
).json().get("url", "#")

html = f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'>
<title>Today's Guide: {topic}</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 700px; margin: 60px auto; padding: 20px; color: #222; }}
  h1 {{ color: #1a1a2e; }}
  .buy-btn {{ display: block; width: fit-content; margin: 30px auto; padding: 16px 32px;
    background: #635bff; color: white; text-decoration: none; border-radius: 8px;
    font-size: 18px; font-weight: bold; }}
  .preview {{ opacity: 0.5; filter: blur(3px); user-select: none; }}
</style></head>
<body>
<h1>📘 {topic}</h1>
<p><em>Published: {today}</em></p>
{chr(10).join(f'<p>{line}</p>' for line in content.split(chr(10))[:6])}
<div class='preview'>
{chr(10).join(f'<p>{line}</p>' for line in content.split(chr(10))[6:])}
</div>
<a class='buy-btn' href='{stripe_link}'>🔓 Get Full Guide — $4.99</a>
</body></html>"""

with open("docs/index.html", "w") as f:
    f.write(html)

print(f"✅ Published: {topic}")
