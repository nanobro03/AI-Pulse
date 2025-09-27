Cyberjaya Road Incident Dashboard (VS Code Guide)
A Streamlit web application that visualizes road incident data from a Supabase database. This guide provides setup and run instructions specifically for the Visual Studio Code editor.
Prerequisites
Visual Studio Code
Python 3.8+
Python Extension for VS Code (Install it from the Extensions tab in VS Code).
Setup Instructions
Follow these steps to get your project running.
1. Open the Project Folder in VS Code
This is the most important step. Do not just open the app.py file.
In VS Code, go to File > Open Folder...
Select your main project folder (e.g., DataVisualization).
2. Create the Virtual Environment
If you don't already have a venv folder, create one from the VS Code terminal.
Open a new terminal in VS Code (Terminal > New Terminal or `Ctrl+Shift+``).
Run the following command. You will see a new venv folder appear in the file explorer.
code
Powershell
python -m venv venv
3. Select the Python Interpreter (The VS Code Way)
This is the key step that automates activation.
Press Ctrl+Shift+P to open the Command Palette.
Type Python: Select Interpreter and press Enter.
A list of available interpreters will appear. Choose the one that has .\venv\Scripts\python.exe in its path. It's usually marked with a ⭐ (Recommended) star.
![alt text](https://code.visualstudio.com/assets/docs/python/environments/interpreter-in-action.gif)
Once you do this, VS Code now knows that this project belongs to this venv. Every new terminal you open will now automatically activate the environment. You'll see (venv) in the prompt.
4. Install Required Packages
Now that VS Code is managing your environment:
Open a new terminal (Terminal > New Terminal). It should automatically show (venv) at the prompt.
Install all the necessary libraries from the requirements.txt file.
code
Powershell
pip install -r requirements.txt
Troubleshooting: If you see a red error about scripts being disabled, run this one-time command in the terminal and then try the pip command again:
code
Powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
5. Set Up Environment Variables
Create a new file in the project folder named exactly .env
Open the .env file and add your Supabase credentials:
code
Code
SUPABASE_URL="your_supabase_url_here"
SUPABASE_KEY="your_supabase_public_api_key_here"
6. Add Incident Photos
Ensure a folder named incident_photos exists in the project.
Place your image files (.jpg, .png) inside this folder.
Rename each image file to match the incident id (e.g., 27.jpg).
Running the Application
With the setup complete, running the app is simple.
Option 1: Using the Terminal (Recommended)
Open a new terminal in VS Code (Terminal > New Terminal).
VS Code will automatically activate your (venv).
Run the app:
code
Powershell
streamlit run app.py
Option 2: Using the "Run and Debug" Feature
For a one-click run experience, you can configure VS Code's debugger.
Go to the "Run and Debug" tab (the bug icon with a play button).
Click "create a launch.json file" and select "Module".
When prompted for the module, enter streamlit.
VS Code will create a .vscode/launch.json file. Replace its content with this:
code
JSON
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
Save the file. Now you can just press F5 (or the green play button in the "Run and Debug" tab) to start your app.
