# LangChain Document Loader POC

This project demonstrates a modular approach to using LangChain's document loader, designed for easy integration into ETL frameworks.

## Features
- Modular document loading using LangChain
- Easy-to-extend structure for ETL integration

## Getting Started
1. Set up a Python environment (e.g., `venv` or `conda`).
2. Install dependencies:
   ```sh
   pip install langchain
   ```
3. Run the main script:
   ```sh
   python main.py
   ```

## Structure
- `main.py`: Entry point for the POC
- `document_loader.py`: Contains reusable document loading logic

## Integration
The code is structured to allow easy import of the document loader module into other ETL pipelines or frameworks.
