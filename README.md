# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# ⚙️ 5. Configuration Setup

This project uses environment variables to configure runtime behavior. All configuration values are loaded from a `.env` file.

## Create the `.env` File

A `.env.template` file is included in the project. Create your `.env` file by copying the template:

**On Linux/macOS (Bash):**

```bash
cp .env.template .env

```

**On Windows (PowerShell):**

```powershell
copy .env.template .env

```

Open the `.env` file and fill in the required values.

---

## 🛠️ Required Environment Variables

| Variable | Description |
| --- | --- |
| `CALCULATE_BASE_DIR` | Base directory for logs and history storage |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of calculations stored in memory |
| `CALCULATOR_AUTO_SAVE` | Automatically save history after each calculation (`true` / `false`) |
| `CALCULATOR_PRECISION` | Decimal precision for floating point results |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed numeric input |
| `CALCULATOR_DEFAULT_ENCODING` | File encoding (e.g., `utf-8`) |
| `CALCULATOR_LOG_DIR` | Directory where logs are stored |
| `CALCULATOR_LOG_FILE` | Log file name |
| `CALCULATOR_HISTORY_DIR` | Directory where history is saved |
| `CALCULATOR_HISTORY_FILE` | History CSV filename |

---

## 💡 Example `.env` Configuration

```env
CALCULATE_BASE_DIR=.
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=4
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_DIR=history
CALCULATOR_HISTORY_FILE=calculator_history.csv

```

> [!CAUTION]
> **⚠️ Do NOT commit your `.env` file to GitHub.** It should be included in your `.gitignore`.

---

# 🚀 6. Running the Project

After setup and activating your virtual environment, run the application:

```bash
python main.py
```

## 🖥️ Usage Guide

You will enter an interactive command-line calculator (**REPL mode**).

### 📌 Available Commands

| Command | Description |
| --- | --- |
| `add` | Perform addition of two numbers |
| `subtract` | Perform subtraction |
| `multiply` | Perform multiplication |
| `divide` | Perform division |
| `power` | Raise $a$ to the power of $b$ |
| `root` | Compute the $b$-th root of $a$ |
| `modulus` | Check divisibility of $a$ with respect to $b$ |
| `int_divide` | Perform integer division |
| `percent` | Calculate what percent of $b$ is $a$ |
| `abs_diff` | Compute absolute difference |
| `help` | Show all available commands |
| `history` | Show calculation history |
| `clear` | Clear calculation history |
| `undo` | Undo last calculation |
| `redo` | Redo last undone calculation |
| `save` | Save history to file |
| `load` | Load history from file |
| `exit` | Exit the calculator |

### 🧮 Example Session

```text
> add
Enter first number: 5
Enter second number: 3
Result: 8

> history
1. Addition(5, 3) = 8

> save
History saved successfully.

> exit
Goodbye!

```

---

# 🧪 7. Testing Instructions

This project uses `pytest` for unit testing.

### ▶ Run All Tests

```bash
pytest

```

### 📊 Run Tests with Coverage

```bash
pytest --cov=app --cov-report=term-missing

```

**The coverage report will show:**

* Overall coverage percentage
* Missing lines per file

### 📁 Test Configuration

Test behavior is controlled via `pytest.ini`, which is already included in the project. No additional configuration is required.

---

# 🔁 8. CI/CD – GitHub Actions

This project includes a GitHub Actions workflow that automatically runs on every push and pull request.

### 🚀 What It Does

The workflow performs the following tasks:

1. **Sets up** Python environment.
2. **Installs** project dependencies.
3. **Runs** all unit tests.
4. **Checks** test coverage.
5. **Fails the build** if tests do not pass or coverage is insufficient.

**This ensures:**

* High code quality.
* No broken commits reach the main branch.
* Reliable project stability and continuous validation.

### 📂 Workflow Location

The configuration file is located at:
`.github/workflows/<workflow-file>.yml`

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
