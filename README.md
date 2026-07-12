# 🛠️ aa_tools

**A friendly toolbox of cool functions for kid-built agents.**

`aa_tools` is a Python library that gives your agents super-powers: search the
web, read web pages, send emails, talk to AI, check the weather, translate
languages, grab space pictures from NASA, roll dice, fetch cat facts, and a
whole lot more — **48 functions** in total.

It is written with **only the Python standard library**, so it works inside
[Pyodide](https://pyodide.org) (the Python that runs right in your web
browser) and installs with `micropip`. No compiled wheels, no headaches.

> 🔑 You bring the API keys. We never store them — you just pass them as
> arguments when you call a function.

---

## 🚀 Install

### In a Pyodide / web notebook
```python
import micropip
await micropip.install("aa_tools-0.1.0-py3-none-any.whl")  # or from PyPI
import aa_tools as aa
```

### Normal Python (uv or pip)
```bash
uv pip install aa-tools        # or: pip install aa-tools
```
```python
import aa_tools as aa
```

---

## 🎉 Quick start

```python
import aa_tools as aa

# No key needed - just fun!
print(aa.get_joke())
print(aa.get_cat_fact())
print(aa.get_pokemon("pikachu")["types"])
print(aa.flip_coin())
print(aa.number_fact(7))

# With a key you supply
results = aa.search_web("cute penguins", api_key="YOUR_BRAVE_KEY")
for r in results:
    print(r["title"], "->", r["url"])

reply = aa.ask_ai("Explain recursion like I'm 10", api_key="YOUR_OPENAI_KEY")
print(reply)
```

See every function, with a copy-paste example, in the
**[📖 HTML Reference Page](docs/reference.html)**.

---

## 🧰 What's inside

| Category | Example functions |
| --- | --- |
| 🌐 Web & Search | `search_web`, `search_images`, `fetch_page` |
| ✉️ Email | `send_email`, `send_email_gmail` |
| 🤖 AI & Any API | `ask_ai`, `call_api` (talk to *any* REST API) |
| 🌤️ Weather | `get_weather`, `get_forecast` |
| 🌍 Translate | `translate_text` |
| 📰 News | `get_news`, `top_headlines` |
| 🚀 Space | `space_image`, `near_earth_objects`, `mars_photo` |
| 🐙 GitHub | `github_repo`, `github_user`, `github_search_repos` |
| 🎉 Fun & Games | `get_joke`, `get_cat_fact`, `get_dog_image`, `get_pokemon`, dice & coins |
| 📚 Knowledge | `wikipedia_summary`, `define_word`, `number_fact`, `country_info` |
| 🖼️ Images | `generate_image`, `get_photo`, `random_image` |
| 🧰 Text Tools | `hash_text`, `base64_encode`, `make_qr`, `convert_units`, `is_palindrome` |

---

## 🔑 Where to get API keys

Most "cool" functions need a free key from the service. You only need the ones
you want to use:

- **Brave Search** (web search): https://brave.com/search/api/
- **OpenAI** (AI chat + image generation): https://platform.openai.com/api-keys
- **OpenWeatherMap** (weather): https://openweathermap.org/api
- **NewsAPI** (news): https://newsapi.org/
- **NASA** (space): https://api.nasa.gov/ — use `"DEMO_KEY"` for light use
- **Pexels** (stock photos): https://www.pexels.com/api/
- **Gmail** (email): create an *app password* at https://myaccount.google.com/apppasswords

Functions that need no key at all: `get_joke`, `get_advice`, `get_cat_fact`,
`get_cat_image`, `get_dog_image`, `get_quote`, `roll_dice`, `flip_coin`,
`random_number`, `pick_one`, `get_pokemon`, `wikipedia_summary`, `define_word`,
`number_fact`, `country_info`, `shorten_url`, `random_image`, and all the
**Text Tools**.

---

## 🛠️ Development

```bash
uv build                 # build wheel + sdist
PYTHONPATH=src python make_reference.py   # regenerate docs/reference.html
```

The build produces a pure-Python wheel tagged `py3-none-any`, which is exactly
what `micropip` needs inside Pyodide.

---

Made with 💛 for young coders and the agents they build.
