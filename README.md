# Summarizer-AI

## Auto Run W/ Script

To make starting the server easier, you can create the following helper scripts inside your `backend` folder. These scripts will automatically activate the virtual environment, install/update any missing dependencies, and start the server.

#### Mac / Linux

**1. Make it executable (One-time setup):**
Open your terminal in the `backend` folder and run:

```bash
chmod +x run_server.sh
```

**2. Run the server:**
Whenever you want to start the backend, just open your terminal in the `backend` folder and run:

```bash
./run_server.sh
```

---

#### Windows

**1. Run the server:**
Whenever you want to start the backend, you can either:

- Double-click the `run_server.bat` file in File Explorer.
- OR, open your terminal/command prompt in the `backend` folder and type:
  ```cmd
  run_server.bat
  ```

## Manual Start

### MAC:

To start, make sure you're in the `backend` folder first.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn main:app --reload
```

- **Ctrl + C** to stop the server.

Deactivate the virtual environment:

```bash
deactivate
```

---

### Windows:

To start, make sure you're in the `backend` folder first.

Create a virtual environment:

```cmd
python -m venv venv
```

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

Install dependencies:

```cmd
python -m pip install -r requirements.txt
```

Start the backend server:

```cmd
uvicorn main:app --reload
```

- **Ctrl + C** to stop the server.

Deactivate the virtual environment:

```cmd
deactivate
```

---

### Updating Dependencies

To save your current dependencies into `requirements.txt`:

```bash
pip freeze > requirements.txt
```

```

```
