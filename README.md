# 🚀 ProjectDump

**ProjectDump** is a Python CLI tool that detects a project's technologies, filters out non-essential files, and compiles the source code and directory structure into a single readable file.

---

## 📦 Features

- 🔍 Auto-detects technologies (Python, JavaScript, Java, etc.)
- 🧹 Skips dependencies, binaries, media, and config clutter
- 🌲 Generates a clean directory tree
- 📄 Dumps readable source code with syntax highlighting
- ⚡ Handles large projects and ignores huge files (>100MB)

---

## 🧑‍💻 Supported Technologies (Partial List)

- **Languages**: Python, JS/TS, Java, Kotlin, PHP, Ruby, Go, Rust, C#, Dart, R, Scala, Elixir
- **Frameworks**: React, Vue, Svelte, Angular, Next.js, Nuxt, Flutter, Android, iOS
- **Infra**: Docker, Kubernetes, Terraform, Ansible
- **CI/CD**: GitHub Actions, GitLab CI, CircleCI

---

## 📂 Output Example

```txt
🚀 PROJECTDUMP
========================================
🌐 Select language (en/vi): en
📂 Enter the project folder path: /path/to/your/project
🔍 Analyzing project at: /path/to/your/project
🔍 Scanning directories...
🛠️  Detected technologies: python
📁 Extensions included: .py, .pyi, .pyx
📁 Generating directory tree...
📄 Processing files...
  📝 Processing: aggregator.py
  📝 Processing: constants.py
  📝 Processing: detector.py
  📝 Processing: filters.py
  📝 Processing: one_file_version.py
  📝 Processing: tree_generator.py
  📝 Processing: __main__.py

✅ Success! File created: /path/to/your/project/project_codebase.md

📊 Summary:
   - Files processed: 7
   - Output size: 30275 characters (~28 KB)
   - Total lines: 870

🎉 Done! The project_codebase.md file is ready.
```

Inside `project_codebase.md` demo:

```text
# ==================================================
# Project Path: /path/to/your/project
# Detected Tech: python
# ==================================================

## DIRECTORY STRUCTURE

New folder/
├── __pycache__/
├── __main__.py
├── aggregator.py
├── constants.py
├── detector.py
├── filters.py
├── one_file_version.py
├── project_codebase.md
└── tree_generator.py

## FILE CONTENTS

### __main__.py

import os
...
```

Run from the command line:

```bash
  python main.py /path/to/your/project
```

### 🚅 Faster Ways to Run:

**1. Using the shortcut (Windows):**
Just double-click `run.bat` or run:
```cmd
  run.bat /path/to/your/project
```

**2. As a command (Global):**
Install once:
```bash
  pip install -e .
```
Then run from anywhere:
```bash
  pd /path/to/your/project
```

---

## 🤖 AI-Ready Packaging
ProjectDump is optimized for AI analysis:
- **AI Instructions**: Automatically includes folders like `.cursor`, `.agents`, `.cline`, and `_agent` which are normally ignored by other tools.
- **Clean Architecture**: Better detection for .NET solutions and Clean Architecture patterns (includes `appsettings.json`, `Web.config`, etc.).



## 📁 What It Ignores

- **Dependency folders**: node_modules, venv, etc.

- **Media & binaries**: .jpg, .exe, .log, etc.

- **Config/IDE**: .git, .vscode, .github, etc.

- **Large files over 100MB**

## ✅ Requirements

Python 3.x

## 🤝 Contributing

Feel free to fork and contribute to enhance tech detection, support new stacks, or improve output formatting!
