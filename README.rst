Modular FastAPI Boilerplate
===========================

This repository provides a modular FastAPI boilerplate where **each Git branch is an independent module**.  
Modules are pre-configured FastAPI application templates focused on specific use cases.

For example: 

- ``module/alembic`` = FastAPI + SQLAlchemy + Alembic  
- ``module/alembic-pytest`` = FastAPI + SQLAlchemy + Alembic + Pytest


🚀 How to use
#############

Make sure you have `uv <https://github.com/astral-sh/uv>`_ installed — this boilerplate is built with it in mind (though it also works with ``pip >= 21.1``).

To start a project based on a specific module:

.. code-block:: bash

    git clone -b <module-branch-name> https://github.com/kuyugama/modular-fastapi-boilerplate <your-project-name>
    cd <your-project-name>
    uv venv
    uv sync
    # or pip install -e .

📦 Available Modules
####################

=========================  =========================================================================
Branch                     Description                        
-------------------------  -------------------------------------------------------------------------
``module/sqlalchemy``      Adds SQLAlchemy ORM support(bases: basic)
``module/alembic``         Adds Alembic migrations(bases: module/sqlalchemy)
``module/pytest``          Adds pytest testing setup(bases: basic)
``module/alembic-pytest``  SQLAlchemy + Alembic + Pytest stack(bases: module/alembic, module/pytest)
=========================  =========================================================================

💡 Philosophy
#############

This is **not** a framework.
It's a **starter kit** for developers who want to bootstrap a project with specific tools, without worrying about architecture or boilerplate.

Each module is focused, clean, and conflict-free. No giant monolith, no 100 dependencies you didn’t ask for.
