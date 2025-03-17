# valueNotifier

A stock market tracking Web service.

Formed by Django framework with C++ services.

## Dependency
- cmake
- libcurl. To install
  - On Ubuntu-based systems (e.g., Linux Mint): sudo apt-get install libcurl4-openssl-dev
  - On Fedora-based systems (e.g., CentOS, RHEL): sudo dnf install curl-devel
  - On macOS (using Homebrew): brew install curl
  - On Windows: You can download the libcurl development package from the official website and follow the installation instructions.
- PostgreSQL and libpq-dev. To install
  1. On Ubuntu-based systems (e.g., Linux Mint): `sudo apt install postgresql postgresql-contrib libpq-dev`
  2. On Fedora-based systems (e.g., CentOS, RHEL): `sudo dnf install postgresql-server postgresql-devel
- pqxx (The C++ API for PostgreSQL). To install:
  - For Debian-based systems:
  ```bash
  sudo apt install libpqxx-dev
  ```
- Python prerequisite:
  - psycopg2-binary: for PostgreSQL
  - flask, flask_sqlalchemy: Flask framework