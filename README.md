# 🚀 Modal FastAPI Boilerplate

**Modal FastAPI Boilerplate** is a repository containing multiple 
implementations of a FastAPI-based boilerplate, all built upon a single, unified project structure.

Each implementation is provided via its own Git branch, enabling a better developer experience for both usage and extension.

---

## 🗂️ Project Structure

This boilerplate offers a **simple yet scalable** structure that’s suitable for both production and development use cases:

```
project root
├─ api/
│  ├─ app_factory.py     # FastAPI application factory
│  ├─ constants/         # Shared constants
│  ├─ error_handlers.py  # Error handler registration
│  ├─ error.py           # APIError base class
│  ├─ errors.py          # Common API error definitions
│  ├─ protocols.py       # Typing and Pydantic protocols
│  ├─ route/             # API route definitions
│  ├─ schema/            # Request and response schemas
│  └─ util/              # Common utilities
├─ app_api.py            # Entry point for production
├─ .secrets.yaml         # Secrets: tokens, DB URLs, encryption keys, etc.
└─ settings.yaml         # Application configuration
```
