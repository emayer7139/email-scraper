# email-scraper
A lightweight, Python-based web crawler that visits a site’s publicly linked pages (BFS-style), extracts any visible e-mail addresses via regex, and saves them to a CSV file.

---

## Features

- **One-pass BFS crawl** — starts at your homepage and follows internal links up to a page limit  
- **Email harvesting** — uses a simple, well-tested regex to pull out addresses  
- **Respectful** — optional `robots.txt` support, polite crawl delay  
- **HTTP/HTTPS fallback** — will retry over HTTP if HTTPS fetch fails  
- **Zero dependencies beyond** `requests` and `beautifulsoup4`  

---

## Prerequisites

- Python 3.8+  
- `pip install requests beautifulsoup4 lxml`

---

## Installation

1. Clone or download this repo.  
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
