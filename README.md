````markdown
# HealthForce Test Project

A test project providing CLI tools for:

- **LinkedIn Extractor** – Scrapes posts from a given LinkedIn profile.  
- **Textract Extractor** – Parses invoices and prescriptions from image files.  

Built with Python and [Playwright](https://playwright.dev/python/).

---

## 🚀 Features
- Save LinkedIn login session state locally.
- Extract posts from LinkedIn profiles with customizable post limits.
- Extract text from invoice and prescription images.
- Simple CLI interface with subcommands (`linkedin`, `textract`).

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/your-username/healthforce_test_project.git
cd healthforce_test_project
````

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

## 🔑 LinkedIn Authentication Setup

Playwright requires a logged-in LinkedIn session.
Save your session state by running:

```bash
python save_state.py
```

* A browser window will open.
* Log into LinkedIn manually.
* Press **Enter** in the terminal when done.
* Your session will be saved to `.auth/li_storage_state.json`.

---

## 🖥️ Usage

Run the CLI tool:

```bash
python cli.py [COMMAND] [OPTIONS]
```

### LinkedIn Extractor

Scrape posts from a profile:

```bash
python cli.py linkedin --profile-url https://www.linkedin.com/in/example/ --min-posts 5
```

Arguments:

* `--profile-url` (required) – LinkedIn profile to scrape.
* `--min-posts` (optional, default=5) – Number of posts to extract.

---

### Textract Extractor

Parse invoice and prescription images:

```bash
python cli.py textract --invoice-path samples/invoice.png --rx-path samples/rx.png
```

Arguments:

* `--invoice-path` – Path to invoice image.
* `--rx-path` – Path to prescription image.

---

## 📂 Project Structure

```
healthforce_test_project/
├── cli.py              # CLI entrypoint
├── linkedin.py         # LinkedIn extractor
├── textracter.py       # Textract extractor
├── save_state.py       # Helper to save LinkedIn session state
├── requirements.txt    # Dependencies
├── samples/            # Sample input images
└── .auth/              # Saved LinkedIn session (auto-created)
```

---

## 🛠️ Development

Format code:

```bash
black .
```

Run linter:

```bash
flake8
```
