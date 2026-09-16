# Instagram Username Checker

A Python tool to check if Instagram usernames are available (not registered).

## Features

- **Two checking methods:**
  - **Fast method** (`checker.py`): Uses HTTP requests with BeautifulSoup
  - **Browser method** (`selenium_checker.py`): Uses Selenium with real browser (better at bypassing bot detection)

- Rate limiting & delays between requests
- Randomized User-Agent headers
- Headless browser support
- Automatic WebDriver management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Method 1: HTTP Requests (Fast)

```bash
python checker.py alice bob c00lname123
```

**Output:**
```
[AVAILABLE] alice (status=404, 404 Not Found (likely available))
[TAKEN] bob (status=200, profile page loaded (likely taken))
[UNKNOWN] xyztest (status=429, rate limited (429) - slow down / use proxies)
```

### Method 2: Selenium (More Reliable)

```bash
# Using Chrome (default)
python selenium_checker.py alice bob c00lname123

# Using Firefox
python selenium_checker.py --browser firefox alice bob c00lname123

# Without headless mode (see the browser)
python selenium_checker.py --no-headless alice bob c00lname123

# Custom delays
python selenium_checker.py --min-delay 2.0 --max-delay 5.0 alice bob c00lname123
```

**Output:**
```
[AVAILABLE] alice (No profile found)
[TAKEN] bob (Profile header found (username taken))
[UNKNOWN] xyztest (error: page load timeout)
```

## Important Notes

⚠️ **Respect Instagram's Terms of Service** - Use this tool responsibly.

- Instagram actively blocks automated traffic
- For heavy use, consider:
  - Using rotating proxies
  - Increasing delays between requests
  - Using residential IP addresses
  - Adding real account authentication
  
- Both methods may be rate-limited or blocked by Instagram
- The Selenium method is slower but more resistant to detection

## Configuration

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` with your settings.

## Requirements

- Python 3.8+
- Chrome/Firefox browser
- ChromeDriver or GeckoDriver (automatically managed by `webdriver-manager`)

## License

This project is for educational purposes. Use responsibly.
