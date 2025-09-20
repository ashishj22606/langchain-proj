# Available Data Sources

This project currently supports the following data source types for unstructured data loading:

- text
- pdf
- web
- csv
- json

To add a new source type, register a loader in `document_loader.py` using the `@register_loader` decorator and update this file.
