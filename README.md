# 🚧 AI Pulse Dashboard (VS Code Guide)

A **Streamlit web application** that visualizes road incident data from a **Supabase** database.
This guide provides setup and run instructions specifically for **Visual Studio Code**.

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python 3.8+](https://www.python.org/downloads/)
* **Python Extension for VS Code** (Install from the Extensions tab)

---

## ⚙️ Setup Instructions

### 1. Open the Project Folder in VS Code

> **Important**: Do **not** just open `app.py`.

* In VS Code, go to **File > Open Folder...**
* Select your main project folder.

---

### 2. Create the Virtual Environment

If you don’t already have a `venv` folder:

```terminal
python -m venv venv
```

* Run this in the **VS Code terminal** (`Ctrl+Shift+``).
* A new `venv` folder will appear in the file explorer.

---

### 3. Select the Python Interpreter (VS Code Way)

1. Press **Ctrl+Shift+P** → open **Command Palette**.
2. Search for **Python: Select Interpreter**.
3. Pick the interpreter with:

   ```
   .\venv\Scripts\Activate.ps1
   ```



![Python Interpreter Selection](https://code.visualstudio.com/assets/docs/python/environments/interpreter-in-action.gif)

* Once selected, VS Code will automatically use this environment in every new terminal (`(venv)` will show in the prompt).

---

### 4. Install Required Packages

```terminal
pip install -r requirements.txt
```

> ⚠️ If you see an error about scripts being disabled, run this **once**:


---

## ▶️ Running the Application

### Option 1: Using the Terminal (Recommended)

```terminal
streamlit run app.py
```

