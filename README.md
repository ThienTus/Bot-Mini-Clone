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
   git clone https://github.com/MinhTamNT/image-search-embedding.git
   cd image-search-embedding
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

2. **Search for similar images**:

   - Using an image file:
     ```sh
     curl -X POST -F "file=@path_to_your_image.jpg" http://127.0.0.1:5000/search
     ```
   - Using tags:
     ```sh
     curl -X POST -F "tags=tag1" -F "tags=tag2" http://127.0.0.1:5000/search
     ```

3. **Retrieve tags with pagination**:
   ```sh
   curl -X GET "http://127.0.0.1:5000/tags?page=1&per_page=10"
   ```

## Project Structure

- `main.py`: The main Flask application file.
- `Service/image_service.py`: Contains functions for image processing and embedding extraction.
- `dao/dao.py`: Contains functions for database operations.
- `model.py`: Defines the database models.
- `setup_database.py`: Script for setting up the database.
- `store_vector.py`: Script for computing and storing image embeddings.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
