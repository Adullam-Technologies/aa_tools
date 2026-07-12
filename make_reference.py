"""Generate docs/reference.html - a friendly function reference for kids.

Run with:  python make_reference.py
"""

from __future__ import annotations

import aa_tools as aa

# Each entry: (name, category, description, example, key_arg)
# key_arg is the name of the argument that is a secret/API key (or "" if none).
FUNCTIONS = [
    # ---------------- Web & Search ----------------
    ("search_web", "Web & Search",
     "Search the internet with Brave and get back a tidy list of results (title, link, snippet).",
     'results = aa.search_web("best robots for kids", api_key="YOUR_BRAVE_KEY")\nfor r in results:\n    print(r["title"], "->", r["url"])',
     "api_key"),
    ("search_images", "Web & Search",
     "Search for pictures on the web using Brave Search.",
     'pics = aa.search_images("puppies", api_key="YOUR_BRAVE_KEY")\nprint(pics[0]["url"])',
     "api_key"),
    ("fetch_page", "Web & Search",
     "Download any web page and turn it into clean text (Markdown). Great for reading articles.",
     'text = aa.fetch_page("https://en.wikipedia.org/wiki/Penguin")\nprint(text[:300])',
     ""),

    # ---------------- Email ----------------
    ("send_email", "Email",
     "Send a plain-text email through almost any email provider's SMTP server.",
     'aa.send_email(\n    to="friend@example.com",\n    subject="Hello from my agent!",\n    body="My robot wrote this.",\n    smtp_host="smtp.gmail.com",\n    username="you@gmail.com",\n    password="app-password",\n)',
     "password"),
    ("send_email_gmail", "Email",
     "Send an email using a Gmail account (use a 16-character app password).",
     'aa.send_email_gmail(\n    to="friend@example.com",\n    subject="hi!",\n    body="sent from aa_tools",\n    gmail="you@gmail.com",\n    app_password="abcd efgh ijkl mnop",\n)',
     "app_password"),

    # ---------------- AI & Any API ----------------
    ("ask_ai", "AI & Any API",
     "Chat with an OpenAI-compatible AI model (OpenAI, Groq, Together, and more).",
     'reply = aa.ask_ai("Tell me a fun fact about space", api_key="YOUR_OPENAI_KEY")\nprint(reply)',
     "api_key"),
    ("call_api", "AI & Any API",
     "Call almost ANY REST API in one line. You just give it the URL and (if needed) a key.",
     'data = aa.call_api(\n    "https://api.github.com/repos/octocat/Hello-World",\n    key_header="Accept",\n    key_prefix="application/vnd.github+json",\n)\nprint(data["stargazers_count"])',
     "api_key"),

    # ---------------- Weather ----------------
    ("get_weather", "Weather",
     "Get the current weather for any city in the world (OpenWeatherMap).",
     'w = aa.get_weather("London", api_key="YOUR_OWM_KEY")\nprint(f"{w[\'temp\']}°C and {w[\'description\']}")',
     "api_key"),
    ("get_forecast", "Weather",
     "Get a short multi-day forecast for a city (OpenWeatherMap).",
     'fc = aa.get_forecast("Tokyo", api_key="YOUR_OWM_KEY", days=3)\nprint(fc)',
     "api_key"),

    # ---------------- Translate ----------------
    ("translate_text", "Translate",
     "Translate text into another language. No key needed for small amounts (MyMemory).",
     'print(aa.translate_text("Hello, world!", to_lang="fr"))',
     "api_key"),

    # ---------------- News ----------------
    ("get_news", "News",
     "Search recent news articles about any topic (NewsAPI).",
     'for a in aa.get_news("climate", api_key="YOUR_NEWSAPI_KEY"):\n    print(a["title"])',
     "api_key"),
    ("top_headlines", "News",
     "Get today's top headlines for a country (NewsAPI).",
     'for h in aa.top_headlines(api_key="YOUR_NEWSAPI_KEY", country="us"):\n    print(h["title"])',
     "api_key"),

    # ---------------- Space ----------------
    ("space_image", "Space",
     "Get NASA's Astronomy Picture of the Day (no key needed for light use).",
     'pic = aa.space_image()\nprint(pic["title"], pic["url"])',
     "api_key"),
    ("near_earth_objects", "Space",
     "List asteroids flying near Earth in a date range (NASA NeoWs).",
     'aa.near_earth_objects(api_key="DEMO_KEY", start_date="2024-01-01", end_date="2024-01-07")',
     "api_key"),
    ("mars_photo", "Space",
     "Fetch a real photo taken by a rover on Mars (NASA).",
     'print(aa.mars_photo(sol=1000, api_key="DEMO_KEY"))',
     "api_key"),

    # ---------------- GitHub ----------------
    ("github_repo", "GitHub",
     "Get info about a GitHub repository (stars, language, open issues).",
     'info = aa.github_repo("pallets/flask")\nprint(info["stars"], "stars")',
     "api_key"),
    ("github_user", "GitHub",
     "Get public profile info for a GitHub user.",
     'print(aa.github_user("octocat"))',
     "api_key"),
    ("github_search_repos", "GitHub",
     "Search GitHub repositories by keyword.",
     'for r in aa.github_search_repos("game engine"):\n    print(r["name"], r["stars"])',
     "api_key"),

    # ---------------- Fun & Games ----------------
    ("get_joke", "Fun & Games",
     "Get a random, clean joke with a setup and punchline.",
     'j = aa.get_joke()\nprint(j["setup"]); print(j["punchline"])',
     ""),
    ("get_advice", "Fun & Games",
     "Get a random piece of (silly but wise) advice.",
     'print(aa.get_advice())',
     ""),
    ("get_cat_fact", "Fun & Games",
     "Get a random fact about cats.",
     'print(aa.get_cat_fact())',
     ""),
    ("get_cat_image", "Fun & Games",
     "Get a link to a random photo of a cat.",
     'print(aa.get_cat_image())',
     ""),
    ("get_dog_image", "Fun & Games",
     "Get a random photo of a good dog.",
     'print(aa.get_dog_image())',
     ""),
    ("get_quote", "Fun & Games",
     "Get an inspirational quote and who said it.",
     'q = aa.get_quote()\nprint(f\'"{q["text"]}" - {q["author"]}\')',
     ""),
    ("roll_dice", "Fun & Games",
     "Roll a die with any number of sides (default 6).",
     'print(aa.roll_dice(20))',
     ""),
    ("flip_coin", "Fun & Games",
     "Flip a coin: returns 'heads' or 'tails'.",
     'print(aa.flip_coin())',
     ""),
    ("random_number", "Fun & Games",
     "Pick a random whole number between two values.",
     'print(aa.random_number(1, 100))',
     ""),
    ("pick_one", "Fun & Games",
     "Randomly pick one item from the ones you list.",
     'print(aa.pick_one("red", "green", "blue"))',
     ""),
    ("get_pokemon", "Fun & Games",
     "Look up a Pokémon by name: its type, height, and a picture.",
     'p = aa.get_pokemon("charizard")\nprint(p["name"], p["types"])',
     ""),

    # ---------------- Knowledge ----------------
    ("wikipedia_summary", "Knowledge",
     "Get a short, friendly summary of almost any Wikipedia topic.",
     'info = aa.wikipedia_summary("Aurora")\nprint(info["summary"])',
     ""),
    ("define_word", "Knowledge",
     "Get the dictionary definition and an example sentence for a word.",
     'd = aa.define_word("serendipity")\nprint(d["definitions"][0])',
     ""),
    ("number_fact", "Knowledge",
     "Get a fun, fact-packed description of any number (works offline!).",
     'print(aa.number_fact(7))',
     ""),
    ("country_info", "Knowledge",
     "Get a friendly snapshot of a country using Wikipedia.",
     'c = aa.country_info("Japan")\nprint(c["summary"][:80])',
     ""),
    ("convert_money", "Knowledge",
     "Convert money between currencies using live rates (no key needed).",
     'print(aa.convert_money(10, "USD", "EUR"))',
     ""),
    ("shorten_url", "Knowledge",
     "Make a long URL short using the free is.gd service.",
     'print(aa.shorten_url("https://example.com/very/long/path"))',
     ""),

    # ---------------- Images ----------------
    ("generate_image", "Images",
     "Create an image from a text description using OpenAI DALL·E.",
     'url = aa.generate_image("a robot riding a unicorn on the moon", api_key="YOUR_OPENAI_KEY")\nprint(url)',
     "api_key"),
    ("get_photo", "Images",
     "Search free stock photos on Pexels and get image links.",
     'for url in aa.get_photo("mountains", api_key="YOUR_PEXELS_KEY"):\n    print(url)',
     "api_key"),
    ("random_image", "Images",
     "Get a random photo of any size (no key needed).",
     'print(aa.random_image(width=600, height=400, seed="sunset"))',
     ""),

    # ---------------- Text Tools ----------------
    ("hash_text", "Text Tools",
     "Turn text into a fixed 'fingerprint' hash (sha256 by default).",
     'print(aa.hash_text("hello"))',
     ""),
    ("base64_encode", "Text Tools",
     "Encode text into Base64 (a common way to pack data).",
     'print(aa.base64_encode("hi"))',
     ""),
    ("base64_decode", "Text Tools",
     "Decode Base64 text back to normal text.",
     'print(aa.base64_decode("aGk="))',
     ""),
    ("make_qr", "Text Tools",
     "Make a QR code image for text or a link (returns a URL).",
     'print(aa.make_qr("https://example.com"))',
     ""),
    ("convert_units", "Text Tools",
     "Convert between length or weight units.",
     'print(aa.convert_units(1, "mi", "km"))  # ~1.609\nprint(aa.convert_units(1, "kg", "lb"))  # ~2.205',
     ""),
    ("count_words", "Text Tools",
     "Count how many words are in some text.",
     'print(aa.count_words("one two three"))',
     ""),
    ("reverse_text", "Text Tools",
     "Reverse a string backwards.",
     'print(aa.reverse_text("abc"))  # cba',
     ""),
    ("is_palindrome", "Text Tools",
     "Is the text the same forwards and backwards?",
     'print(aa.is_palindrome("Racecar"))  # True',
     ""),
]

CATEGORIES = [
    "Web & Search", "Email", "AI & Any API", "Weather", "Translate", "News",
    "Space", "GitHub", "Fun & Games", "Knowledge", "Images", "Text Tools",
]

EMOJI = {
    "Web & Search": "🌐", "Email": "✉️", "AI & Any API": "🤖", "Weather": "🌤️",
    "Translate": "🌍", "News": "📰", "Space": "🚀", "GitHub": "🐙",
    "Fun & Games": "🎉", "Knowledge": "📚", "Images": "🖼️", "Text Tools": "🧰",
}

ERRORS = {"AAError", "AARequestError"}
public_funcs = [f for f in aa.list_functions() if f not in ERRORS]
assert {n for n, *_ in FUNCTIONS} == set(public_funcs), (
    f"mismatch: {set(public_funcs) ^ {n for n, *_ in FUNCTIONS}}"
)


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


CSS = """
:root{
  --bg:#fdf6ec; --card:#ffffff; --ink:#2b2b3a; --muted:#6b6b80;
  --brand:#ff7a59; --brand2:#ffb347; --accent:#5b8def; --line:#ffe2c2;
  --shadow:0 10px 30px rgba(255,122,89,.12);
}
*{box-sizing:border-box}
body{
  margin:0; font-family:"Nunito",ui-rounded,"Segoe UI",system-ui,-apple-system,sans-serif;
  background:var(--bg); color:var(--ink); line-height:1.55;
}
header.hero{
  background:linear-gradient(135deg,var(--brand),var(--brand2));
  color:#fff; padding:48px 20px 60px; text-align:center;
  border-bottom-left-radius:36px; border-bottom-right-radius:36px;
}
header.hero h1{font-size:clamp(28px,5vw,46px); margin:0 0 8px; letter-spacing:-.5px}
header.hero p{font-size:clamp(15px,2.4vw,19px); margin:0 auto; max-width:680px; opacity:.95}
.wrap{max-width:1080px; margin:0 auto; padding:0 18px 80px}
.controls{position:sticky; top:0; z-index:5; background:var(--bg);
  padding:18px 0 10px; display:flex; gap:10px; flex-wrap:wrap; align-items:center}
#search{flex:1 1 240px; min-width:200px; padding:12px 16px; border:2px solid var(--line);
  border-radius:999px; font-size:16px; outline:none; background:#fff}
#search:focus{border-color:var(--brand)}
.chips{display:flex; gap:8px; flex-wrap:wrap}
.chip{border:2px solid var(--line); background:#fff; color:var(--muted);
  padding:7px 14px; border-radius:999px; cursor:pointer; font-weight:700; font-size:14px}
.chip.active{background:var(--brand); color:#fff; border-color:var(--brand)}
section.cat{margin-top:34px}
section.cat h2{font-size:24px; display:flex; align-items:center; gap:10px; margin:0 0 14px}
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:18px}
.card{background:var(--card); border:1px solid var(--line); border-radius:20px;
  padding:18px 18px 16px; box-shadow:var(--shadow); display:flex; flex-direction:column}
.card h3{margin:0 0 6px; font-size:18px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.card .desc{color:var(--muted); font-size:14.5px; margin:0 0 12px; flex:1}
pre{background:#2b2b3a; color:#f4f4f8; padding:12px 14px; border-radius:12px;
  overflow:auto; font-size:12.5px; margin:0 0 10px; position:relative}
.copy{position:absolute; top:8px; right:8px; border:none; background:var(--brand);
  color:#fff; border-radius:8px; padding:4px 10px; font-size:12px; cursor:pointer; font-weight:700}
.badge{display:inline-block; font-size:11px; font-weight:800; letter-spacing:.3px;
  padding:3px 9px; border-radius:999px; text-transform:uppercase}
.badge.key{background:#ffe1e1; color:#c0341d}
.badge.free{background:#e3f6e8; color:#1f7a3d}
footer{text-align:center; color:var(--muted); font-size:14px; padding:30px 18px 60px}
a{color:var(--accent)}
.hidden{display:none!important}
"""

JS = """
const cards=[...document.querySelectorAll('.card')];
const chips=document.querySelectorAll('.chip');
const search=document.getElementById('search');
function apply(){
  const q=search.value.trim().toLowerCase();
  const cat=document.querySelector('.chip.active').dataset.cat;
  cards.forEach(c=>{
    const hay=(c.dataset.name+' '+c.dataset.desc+' '+c.dataset.cat).toLowerCase();
    const okCat = cat==='All' || c.dataset.cat===cat;
    const okQ = !q || hay.includes(q);
    c.classList.toggle('hidden', !(okCat&&okQ));
  });
  document.querySelectorAll('section.cat').forEach(s=>{
    const vis=[...s.querySelectorAll('.card')].some(c=>!c.classList.contains('hidden'));
    s.classList.toggle('hidden',!vis);
  });
}
search.addEventListener('input',apply);
chips.forEach(ch=>ch.addEventListener('click',()=>{
  chips.forEach(x=>x.classList.remove('active'));
  ch.classList.add('active'); apply();
}));
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',()=>{
  navigator.clipboard.writeText(b.dataset.code);
  const t=b.textContent; b.textContent='Copied!';
  setTimeout(()=>b.textContent=t,1200);
}));
apply();
"""

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>aa_tools - Function Reference for Kid Coders</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <h1>🛠️ aa_tools Reference</h1>
  <p>Super-power your agent! Every function below works inside Pyodide (the Python that runs in your browser).
  You bring the API keys - we never store them.</p>
</header>
<div class="wrap">
  <div class="controls">
    <input id="search" type="text" placeholder="🔎 Search functions (try 'email', 'cat', 'weather')...">
    <div class="chips">
      <span class="chip active" data-cat="All">All</span>
      {''.join(f'<span class="chip" data-cat="{c}">{EMOJI.get(c,"")} {esc(c)}</span>' for c in CATEGORIES)}
    </div>
  </div>
"""

# Build cards grouped by category
for cat in CATEGORIES:
    items = [(n, d, ex, k) for (n, c, d, ex, k) in FUNCTIONS if c == cat]
    if not items:
        continue
    HTML += f'<section class="cat" id="cat-{esc(cat)}"><h2>{EMOJI.get(cat,"")} {esc(cat)}</h2><div class="grid">'
    for name, desc, example, key in items:
        badge = '<span class="badge key">needs key</span>' if key else '<span class="badge free">free</span>'
        HTML += (
            f'<div class="card" data-name="{esc(name)}" data-desc="{esc(desc)}" data-cat="{esc(cat)}">'
            f'<h3>{esc(name)}()</h3>'
            f'<div class="desc">{esc(desc)}</div>'
            f'<pre><button class="copy" data-code="{esc(example)}">Copy</button>{esc(example)}</pre>'
            f'{badge}</div>'
        )
    HTML += "</div></section>"

HTML += f"""
</div>
<footer>
  Made with 💛 for kid coders · <strong>aa_tools</strong> v{aa.__version__} · {len(FUNCTIONS)} functions<br>
  Tip: install in Pyodide with <code>await micropip.install('aa_tools-0.1.0-py3-none-any.whl')</code> then <code>import aa_tools as aa</code>.
</footer>
<script>{JS}</script>
</body>
</html>
"""

if __name__ == "__main__":
    import os

    os.makedirs("docs", exist_ok=True)
    with open("docs/reference.html", "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Wrote docs/reference.html ({len(HTML)} bytes, {len(FUNCTIONS)} functions)")
