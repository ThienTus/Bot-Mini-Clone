# Bot Mini-Clone

This project implements a production-ready daily ingestion pipeline for OptiSigns support content. It automatically scrapes articles from support.optisigns.com, normalizes them into clean Markdown, and incrementally uploads only new or updated documents into an OpenAI Vector Store powering an OptiBot-style customer support assistant. The pipeline is containerized with Docker, runs as a scheduled batch job on DigitalOcean, and provides structured logs (added, updated, skipped) for traceability and operational visibility.

## Features

- Ingest messy web content and normalize.
- Build Assistant & Programmatically Load Vector Store (API upload is mandatory—no UI drag-and-drop here).
- Deploy Scraper as Daily Job on DigitalOcean Platform.

## Technologies Used

- ![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

## Requirements

- Python 3.10 or higher

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/ThienTus/Bot-Mini-Clone.git
   ```

2. **Create a virtual environment and activate it**:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Flask application**:

   ```sh
   python main.py
   ```

2. **Run Docker**:

   ```sh
   docker build -t optibot-daily-job .

   docker run --rm `
       -e OPENAI_API_KEY=sk-xxx`
       -e ASSISTANT_ID=asst_xxx `
       -e VECTOR_STORE_ID=vs_xxx`
       optibot-daily-job
   ```

## Project Structure

- `main.py`: The main Flask application file.
- `clean_markdown.py`: Convert each article to clean Markdown.
- `markdown.py`: Markdown ≥ 30 articles from support.optisigns.com.
- `init_vector_store.py`: Create ID vector store.
- `upload_to_openai.py`: Upload Markdown files to OpenAI Vector Store files via OpenAI API.
- `zendesk.py`: Zendesk API to read the article.

## Deployment (Daily Job)

The scraper and uploader are packaged as a Dockerized worker job.

- The job re-scrapes OptiSigns support articles daily
- Detects new or updated articles via content hash
- Uploads only deltas to the OpenAI Vector Store
- Logs added, updated, and skipped article counts

Daily Job Logs:

- Last run log (Docker): log/daily_job.log
- Log includes: added / updated / skipped counts

## DigitalOcean Platform

This worker is designed to be triggered daily.
In production, it can be scheduled via DigitalOcean App Platform jobs or external cron trigger.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.
