
# Citadel (LIS) 🧪⚙️

> **Status:** 🚧 Work in Progress (WIP) / Active Beta

> Professional-grade Laboratory Information System (LIS) built with Domain-Driven Design (DDD), Hexagonal Architecture, and a reactive PyQt6 MVVM frontend.

> This repository contains the modern evolution (Citadel LIS) and historical backups of the CastLab legacy system.

---

## 🏛️ Architecture & Design Principles

Citadel LIS is engineered around strict architectural boundaries to ensure long-term maintainability, testability, and enterprise-grade reliability:

* **Hexagonal Architecture (Ports & Adapters):** Core domain logic is completely isolated from external frameworks (Database, GUI, and PDF generation).
* **Domain-Driven Design (DDD):** Encapsulates core medical workflows, state machines for sample validation, and strict clinical business rules (e.g., preventing PDF generation on unvalidated samples).
* **MVVM (Model-View-ViewModel):** Decouples the PyQt6 graphical interface from application services using reactive signals (`pyqtSignal`).
* **Auditability & RBAC:** Enforces strict role-based access control (Bioanalyst vs. Assistant) and immutable audit trails.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Database & ORM:** SQLite (WAL mode) with SQLModel / SQLAlchemy
* **GUI Framework:** PyQt6 (`pytest-qt` for headless testing)
* **Reporting Engine:** ReportLab (Dynamic PDF clinical reports with panic-value highlighting)
* **Testing Framework:** Pytest

---

## 📂 Project Structure

```text
citadel/
├── core/                # Domain entities, value objects, domain exceptions & ports
├── infrastructure/      # Repositories (SQLModel), database setup, & PDF exporters
├── application/         # Use cases, application services (Patient, Sample, Report)
├── presentation/        # PyQt6 Views, ViewModels, and UI components
└── tests/               # Comprehensive automated test suite (Core, Infra, App, GUI)

```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/citadel-lis.git](https://github.com/your-username/citadel-lis.git)
cd citadel-lis

```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install pyqt6 pytest-qt reportlab sqlmodel pytest

```

---

## 🧪 Running the Test Suite

Citadel LIS features a fully automated test suite covering domain logic, database persistence, state transitions, report validation rules, and headless viewmodels:

```bash
python -m pytest -v

```

---

## 🖥️ Running the Application

To launch the composition root, bootstrap the database schema, and run the main PyQt6 GUI application:

```bash
python run.py

```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

