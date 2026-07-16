# 🛠️ aa_agent_tools

**A friendly toolbox of cool functions for kid-built agents.**

`aa_agent_tools` gives your Python agents super-powers: search the web, read pages,
send emails, check the weather, grab space pictures from NASA, roll dice, fetch
cat facts, and a whole lot more — **38 functions**, all listed below with
copy-paste examples.

> 🔑 **You bring the API keys.** We never store them. Just pass them as
> arguments when you call a function. Look for the 🔑 badge below (those need a
> key) and the 🆓 badge (those are totally free, no key at all!).

---

## 🎉 Quick start

```python
import aa_agent_tools as aa

# No key needed — just fun!
print(aa.get_joke())
print(aa.get_cat_fact())
print(aa.get_pokemon("pikachu")["types"])
print(aa.flip_coin())
print(aa.number_fact(7))

# With a key you supply
results = aa.search_web("cute penguins", api_key="YOUR_BRAVE_KEY")
print(results)
```

Want the pretty, searchable version? Open the
**[📖 HTML Reference Page](docs/reference.html)** in your browser.

---

## 📖 The full function reference

Every function is listed below, grouped by what it does. Each one shows a
short, friendly description and a copy-paste example you can try right away.

- 🔑 = needs an API key (you pass it as an argument)
- 🆓 = totally free, no key needed

---

### 🌐 Web & Search

#### `search_web(query, api_key)` 🔑
Search the internet with Brave and get back a tidy list of results (title,
link, snippet).

```python
results = aa.search_web("best robots for kids", api_key="YOUR_BRAVE_KEY")
print(results)
```

#### `search_images(query, api_key, count=5)` 🔑
Search for pictures on the web using Brave Search.

```python
pics = aa.search_images("puppies", api_key="YOUR_BRAVE_KEY")
print(pics[0]["url"])
```

#### `fetch_page(url)` 🆓
Download any web page and turn it into clean text (Markdown). Great for reading
articles.

```python
text = aa.fetch_page("https://en.wikipedia.org/wiki/Penguin")
print(text[:300])
```

---

### ✉️ Email

#### `send_email(to, subject, body, *, smtp_host, username, password)` 🔑
Send a plain-text email through almost any email provider's SMTP server.

```python
aa.send_email(
    to="friend@example.com",
    subject="Hello from my agent!",
    body="My robot wrote this.",
    smtp_host="smtp.gmail.com",
    username="you@gmail.com",
    password="app-password",
)
```

#### `send_email_gmail(to, subject, body, *, gmail, app_password)` 🔑
Send an email using a Gmail account (use a 16-character app password).

```python
aa.send_email_gmail(
    to="friend@example.com",
    subject="hi!",
    body="sent from aa_agent_tools",
    gmail="you@gmail.com",
    app_password="abcd efgh ijkl mnop",
)
```

---

### 🤖 Any API

#### `call_api(url, api_key=None, *, method="GET", ...)` 🆓
Call almost **any** REST API in one line. You give it a URL and (if the API
needs one) a key. No key needed for public APIs.

```python
city = input("Enter your city: ")
data = aa.call_api(
	"https://api.weatherapi.com/v1/current.json?key=key&q={city}&aqi=no"	
)

current = data["current"]
	
print(current["temp_c"])
```

---

### 🌤️ Weather

#### `get_weather(city, api_key)` 🔑
Get the current weather for any city in the world (OpenWeatherMap).

```python
w = aa.get_weather("London", api_key="YOUR_OWM_KEY")
print(f"{w['temp']}°C and {w['description']}")
```

#### `get_forecast(city, api_key, days=3)` 🔑
Get a short multi-day forecast for a city (OpenWeatherMap).

```python
fc = aa.get_forecast("Tokyo", api_key="YOUR_OWM_KEY", days=3)
print(fc)
```

---

### 🚀 Space

#### `space_image(date=None, api_key="DEMO_KEY")` 🆓
Get NASA's Astronomy Picture of the Day (`"DEMO_KEY"` works for light use).

```python
pic = aa.space_image()
print(pic["title"], pic["url"])
```

#### `near_earth_objects(api_key="DEMO_KEY", *, start_date=None)` 🆓
List asteroids flying near Earth in a date range (NASA NeoWs).

```python
aa.near_earth_objects(api_key="DEMO_KEY", start_date="2024-01-01")
```

#### `mars_photo(*, sol=1000, api_key="DEMO_KEY")` 🆓
Fetch a real photo taken by a rover on Mars (NASA).

```python
print(aa.mars_photo(sol=1000, api_key="DEMO_KEY"))
```

---

### 🎉 Fun & Games

#### `get_joke()` 🆓
Get a random, clean joke with a setup and punchline.

```python
j = aa.get_joke()
print(j["setup"]); print(j["punchline"])
```

#### `get_advice()` 🆓
Get a random piece of (silly but wise) advice.

```python
print(aa.get_advice())
```

#### `get_cat_fact()` 🆓
Get a random fact about cats.

```python
print(aa.get_cat_fact())
```

#### `get_cat_image()` 🆓
Get a link to a random photo of a cat.

```python
print(aa.get_cat_image())
```

#### `get_dog_image()` 🆓
Get a random photo of a good dog.

```python
print(aa.get_dog_image())
```

#### `get_quote()` 🆓
Get an inspirational quote and who said it.

```python
q = aa.get_quote()
print(f'"{q["text"]}" - {q["author"]}')
```

#### `roll_dice(sides=6)` 🆓
Roll a die with any number of sides (default 6).

```python
print(aa.roll_dice(20))
```

#### `flip_coin()` 🆓
Flip a coin: returns `"heads"` or `"tails"`.

```python
print(aa.flip_coin())
```

#### `random_number(min_value=1, max_value=100)` 🆓
Pick a random whole number between two values.

```python
print(aa.random_number(1, 100))
```

#### `pick_one(*items)` 🆓
Randomly pick one item from the ones you list.

```python
print(aa.pick_one("red", "green", "blue"))
```

#### `get_pokemon(name="pikachu")` 🆓
Look up a Pokémon by name: its type, height, and a picture.

```python
p = aa.get_pokemon("charizard")
print(p["name"], p["types"])
```

---

### 📚 Knowledge

#### `wikipedia_summary(title)` 🆓
Get a short, friendly summary of almost any Wikipedia topic.

```python
info = aa.wikipedia_summary("Aurora")
print(info["summary"])
```

#### `define_word(word)` 🆓
Get the dictionary definition and an example sentence for a word.

```python
d = aa.define_word("serendipity")
print(d["definitions"][0])
```

#### `number_fact(number)` 🆓
Get a fun, fact-packed description of any number (works offline!).

```python
print(aa.number_fact(7))
```

#### `country_info(name)` 🆓
Get a friendly snapshot of a country using Wikipedia.

```python
c = aa.country_info("Japan")
print(c["summary"][:80])
```

#### `convert_money(amount, from_currency, to_currency)` 🆓
Convert money between currencies using live rates (no key needed).

```python
print(aa.convert_money(10, "USD", "EUR"))
```

#### `shorten_url(url)` 🆓
Make a long URL short using the free is.gd service.

```python
print(aa.shorten_url("https://example.com/very/long/path"))
```

---

### 🖼️ Images

#### `get_photo(query, api_key)` 🔑
Search free stock photos on Pexels and get image links.

```python
for url in aa.get_photo("mountains", api_key="YOUR_PEXELS_KEY"):
    print(url)
```

#### `random_image(*, width=400, height=300, seed=None)` 🆓
Get a random photo of any size (no key needed).

```python
print(aa.random_image(width=600, height=400, seed="sunset"))
```

---

### 🧰 Text Tools

#### `hash_text(text, *, algorithm="sha256")` 🆓
Turn text into a fixed "fingerprint" hash (sha256 by default).

```python
print(aa.hash_text("hello"))
```

#### `base64_encode(text)` 🆓
Encode text into Base64 (a common way to pack data).

```python
print(aa.base64_encode("hi"))
```

#### `base64_decode(text)` 🆓
Decode Base64 text back to normal text.

```python
print(aa.base64_decode("aGk="))
```

#### `make_qr(text, *, size=200)` 🆓
Make a QR code image for text or a link (returns a URL).

```python
print(aa.make_qr("https://example.com"))
```

#### `convert_units(value, from_unit, to_unit)` 🆓
Convert between length or weight units.

```python
print(aa.convert_units(1, "mi", "km"))  # ~1.609
print(aa.convert_units(1, "kg", "lb"))  # ~2.205
```

#### `count_words(text)` 🆓
Count how many words are in some text.

```python
print(aa.count_words("one two three"))
```

#### `reverse_text(text)` 🆓
Reverse a string backwards.

```python
print(aa.reverse_text("abc"))  # cba
```

#### `is_palindrome(text)` 🆓
Is the text the same forwards and backwards?

```python
print(aa.is_palindrome("Racecar"))  # True
```

---

## 🔑 Where to get API keys

Most "cool" functions need a free key from the service. You only need the ones
you want to use:

- **Brave Search** (web & image search): https://brave.com/search/api/
- **OpenWeatherMap** (weather): https://openweathermap.org/api
- **NASA** (space): https://api.nasa.gov/ — use `"DEMO_KEY"` for light use
- **Pexels** (stock photos): https://www.pexels.com/api/
- **Gmail** (email): create an *app password* at https://myaccount.google.com/apppasswords

Functions that need **no key at all**: `get_joke`, `get_advice`, `get_cat_fact`,
`get_cat_image`, `get_dog_image`, `get_quote`, `roll_dice`, `flip_coin`,
`random_number`, `pick_one`, `get_pokemon`, `wikipedia_summary`, `define_word`,
`number_fact`, `country_info`, `convert_money`, `shorten_url`, `random_image`,
`fetch_page`, `call_api` (key optional), and all the **Text Tools**.

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
