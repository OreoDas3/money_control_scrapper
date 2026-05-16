# Moneycontrol Business News Scraper

A modular Python-based web scraping pipeline that extracts **business news articles** from Moneycontrol and loads the scraped data into **Snowflake** for analysis.

## Project Overview

This project scrapes business-related article links from the Moneycontrol homepage, extracts structured article data, and bulk loads the results into Snowflake.

Extracted fields:

- Title
- Author
- Publication Date
- Article URL
- Article Content

The scraper is designed with a modular architecture for maintainability, configurability, and scalability.

---

## Features

- Modular project structure
- YAML-based configuration
- Configurable retry mechanism with exponential backoff
- Parallel article scraping using ThreadPoolExecutor
- Reusable HTTP session for better performance
- Snowflake bulk loading using `write_pandas`
- Dynamic URL filtering using regex
- Handles multiple article page layouts
- Advanced author extraction logic
- Fintech article template handling
- Logging support
- Error handling with retries

---

## Project Structure

```bash
moneycontrol_scraper/
│
├── config.yaml
├── main.py
├── requirements.txt
├── README.md
│
├── common/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── session_manager.py
│
├── scraper/
│   ├── __init__.py
│   ├── fetcher.py
│   ├── link_extractor.py
│   └── article_parser.py
│
├── loader/
│   ├── __init__.py
│   └── snowflake_loader.py
│
└── models/
    ├── __init__.py
    └── article.py
```

---

## Technology Stack

- Python 3.x
- BeautifulSoup
- Requests
- Pandas
- Snowflake Connector
- YAML
- Concurrent Futures

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/money_control_scrapper.git
cd money_control_scrapper
```

---

### 2. Create Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `config.yaml` file:

```yaml
snowflake:
  account: "YOUR_ACCOUNT"
  user: "YOUR_USER"
  password: "YOUR_PASSWORD"
  role: "YOUR_ROLE"
  warehouse: "COMPUTE_WH"
  database: "NEWS_DB"
  schema: "SCRAPING"

scraper:
  homepage_url: "https://www.moneycontrol.com/"
  timeout: 20
  max_retries: 3
  retry_backoff_seconds: 2
  thread_pool_size: 10

headers:
  user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
  accept_language: "en-US,en;q=0.9"

snowflake_load:
  table_name: "ARTICLES"
  recreate_table: true

patterns:
  article_regex: "^https://www\\.moneycontrol\\.com/.*business.*\\.html$"

logging:
  level: "INFO"
```

---

## Running the Project

Run:

```bash
python main.py
```

---

## Data Load Target

Snowflake table:

```sql
NEWS_DB.SCRAPING.ARTICLES
```

Columns:

- ID
- TITLE
- AUTHOR
- PUBLICATION_DATE
- ARTICLE_URL
- CONTENT

---

## URL Filtering Logic

The scraper only processes URLs that:

- belong to `https://www.moneycontrol.com`
- contain the keyword `business`
- end with `.html`

Example valid URLs:

```text
https://www.moneycontrol.com/news/business/markets/article.html
https://www.moneycontrol.com/business/personal-finance/article.html
```

---

## Author Extraction Logic

Supports:

- Named authors
- Multiple authors
- Anchor tag author extraction
- Meta author extraction
- Plain text authors (PTI / Reuters)
- Disclaimer-based author mapping

Special mappings:

| Condition | Output |
|---------|--------|
| external partner | External Source |
| experts on moneycontrol.com | Moneycontrol Experts |

---

## Content Extraction Logic

Supports multiple article templates:

- Standard article pages
- Fintech pages
- Alternate content wrappers
- Live blog layouts

Filters junk content such as:

- advertisements
- social sharing text
- login prompts
- subscription banners

---

## Logging

Example:

```text
INFO - Starting Moneycontrol scraper pipeline
INFO - Filtered business article links: 24
INFO - Total scraped rows: 24
INFO - Successfully loaded 24 rows into Snowflake
```

---

## Future Improvements

- Incremental Snowflake loads
- Duplicate detection
- Unit test coverage
- Dockerization
- CI/CD pipeline
- Airflow orchestration
- Cloud deployment

---

## Security Note

Do not commit `config.yaml` containing credentials.

Add to `.gitignore`:

```gitignore
config.yaml
```

---

## License

For educational and demonstration purposes.