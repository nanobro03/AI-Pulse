# 🚧 Cyberjaya Road Incident Dashboard (VS Code Guide)

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
* Select your main project folder (e.g., `DataVisualization`).

---

### 2. Create the Virtual Environment

If you don’t already have a `venv` folder:

```powershell
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
   .\venv\Scripts\python.exe
   ```

   (usually marked ⭐ *Recommended*).

![Python Interpreter Selection](https://code.visualstudio.com/assets/docs/python/environments/interpreter-in-action.gif)

* Once selected, VS Code will automatically use this environment in every new terminal (`(venv)` will show in the prompt).

---

### 4. Install Required Packages

```powershell
pip install -r requirements.txt
```

> ⚠️ If you see an error about scripts being disabled, run this **once**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

### 5. Set Up Environment Variables

Create a new file in your project root called **`.env`** and add:

```env
SUPABASE_URL="your_supabase_url_here"
SUPABASE_KEY="your_supabase_public_api_key_here"
```

---

### 6. Add Incident Photos

* Create a folder named **`incident_photos`** in your project.
* Place your image files (`.jpg`, `.png`) inside.
* Rename each file to match the **incident id** (e.g., `27.jpg`).

---

## ▶️ Running the Application

### Option 1: Using the Terminal (Recommended)

```powershell
streamlit run app.py
```

### Option 2: Using "Run and Debug"

1. Go to **Run and Debug** tab in VS Code.
2. Click **create a launch.json file** → choose **Module**.
3. Enter `streamlit` when asked for module name.
4. Replace the auto-generated `.vscode/launch.json` with:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Streamlit",
      "type": "python",
      "request": "launch",
      "module": "streamlit",
      "args": [
        "run",
        "app.py"
      ]
    }
  ]
}
```

* Now you can press **F5** (or the green ▶ button) to run the app.

---

## 📂 Project Structure

```
.
├── incident_photos/
│   ├── 1.jpg
│   ├── 12.png
│   └── ...
├── venv/
├── .vscode/
│   └── launch.json
├── .env
├── app.py
├── requirements.txt
└── README.md
```
