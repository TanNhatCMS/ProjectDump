import fnmatch
import os
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union


def get_essential_files() -> Set[str]:
    return set()


def get_exclude_patterns() -> Tuple[Set[str], Set[str]]:
    exclude_dirs = {
        # Dependencies & environments
        "node_modules",
        "vendor",
        "venv",
        "env",
        ".venv",
        ".env",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "__pycache__",
        ".cache",
        "pip-wheel-metadata",
        "site-packages",
        "deps",
        "packages",
        ".tox",
        # Build artifacts
        "dist",
        "build",
        "target",
        "out",
        "bin",
        "obj",
        ".eggs",
        "lib",
        "lib64",
        "generated",
        # Framework build folders
        ".next",
        ".nuxt",
        ".angular",
        "coverage",
        ".turbo",
        ".vercel",
        ".expo",
        ".parcel-cache",
        # Version control & IDE tools
        ".git",
        ".svn",
        ".hg",
        ".idea",
        ".vscode",
        ".vs",
        ".history",
        ".vscode-test",
        # Temp & OS folders
        "temp",
        "tmp",
        ".tmp",
        ".DS_Store",
        "__MACOSX",
        "Thumbs.db",
        "System Volume Information",
        # CI/CD & Docker volumes
        ".github",
        ".gitlab",
        ".circleci",
        ".docker",
        "logs",
        "log",
        "docker",
        "containers",
        # Database & sessions
        "db",
        "database",
        "sqlite",
        "sessions",
        "flask_session",
        "instance",
    }

    exclude_files = {
        # Logs
        "*.log",
        "*.log.*",
        "*.out",
        # Package manager lock files
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "composer.lock",
        "poetry.lock",
        "Cargo.lock",
        # Compiled/intermediate binaries
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.class",
        "*.o",
        "*.so",
        "*.dll",
        "*.exe",
        "*.dylib",
        "*.a",
        # Media files
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.svg",
        "*.ico",
        "*.webp",
        "*.mp3",
        "*.wav",
        "*.mp4",
        "*.avi",
        "*.mov",
        "*.mkv",
        "*.flac",
        "*.ogg",
        # Fonts
        "*.ttf",
        "*.otf",
        "*.woff",
        "*.woff2",
        # Archives & compressed
        "*.zip",
        "*.tar",
        "*.gz",
        "*.rar",
        "*.7z",
        "*.bz2",
        "*.xz",
        "*.lz",
        "*.lzma",
        # Office / documents
        "*.pdf",
        "*.docx",
        "*.doc",
        "*.ppt",
        "*.pptx",
        "*.xls",
        "*.xlsx",
        "*.csv",
        # OS/system files
        ".DS_Store",
        "Thumbs.db",
        "desktop.ini",
        "ehthumbs.db",
        "Icon\r",
        # Misc config/cache
        "*.env",
        "*.env.*",
        "*.ini",
        "*.toml",
        "*.bak",
        "*.swp",
        "*.swo",
        # ProjectDump output files
        "project_codebase.md",
        "source_dump.txt",
    }

    return exclude_dirs, exclude_files


class GitIgnoreFilter:
    def __init__(self, project_path: Union[str, Path]):
        self.project_path = Path(project_path)
        self.patterns = self._load_gitignore()

    def _load_gitignore(self) -> List[str]:
        patterns = []
        gitignore_path = self.project_path / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Xử lý pattern kết thúc bằng / (thư mục)
                            if line.endswith("/"):
                                patterns.append(line + "*")
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def is_ignored(self, rel_path: str) -> bool:
        """Kiểm tra xem file/thư mục có bị ignore bởi .gitignore không"""
        if not self.patterns:
            return False

        # Chuẩn hóa path sang kiểu unix để match pattern
        normalized_path = rel_path.replace("\\", "/")
        
        for pattern in self.patterns:
            # Xử lý pattern bắt đầu bằng / (root-relative)
            if pattern.startswith("/"):
                p = pattern[1:]
                if fnmatch.fnmatchcase(normalized_path, p) or \
                   fnmatch.fnmatchcase(normalized_path, p + "/*"):
                    return True
            else:
                # Pattern có thể ở bất kỳ đâu
                if fnmatch.fnmatchcase(normalized_path, pattern) or \
                   fnmatch.fnmatchcase(os.path.basename(normalized_path), pattern) or \
                   any(fnmatch.fnmatchcase(part, pattern) for part in normalized_path.split("/")) or \
                   fnmatch.fnmatchcase(normalized_path, "*/" + pattern) or \
                   fnmatch.fnmatchcase(normalized_path, "*/" + pattern + "/*"):
                    return True
        return False


def get_ai_root_patterns() -> Set[str]:
    """Các file hướng dẫn AI ở ROOT được ưu tiên bao gồm"""
    return {
        "ai_instructions.md", "instructions.md", "architecture.md",
        "system_prompt.md", "context.md", "project_rules.md",
        ".clinerules", ".cursorrules", ".windsurfrules", "tasks.md",
        "README.md"
    }


def get_ai_allowlist() -> Set[str]:
    """Các thư mục và file liên quan đến AI instruction không được bị loại bỏ"""
    return {
        ".agents", ".agent", "_agents", "_agent", 
        ".cursor", ".cline", ".ai_instructions", ".clinerules"
    }


def should_exclude_path(
    path: Union[str, Path], 
    exclude_dirs: Set[str], 
    gitignore_filter: Optional[GitIgnoreFilter] = None
) -> bool:
    path_obj = Path(path)
    parts = [p.lower() for p in path_obj.parts]
    
    # ✅ Nếu là thư mục AI thì KHÔNG loại bỏ
    ai_allowlist = get_ai_allowlist()
    if any(p in ai_allowlist for p in parts):
        return False
        
    # Check default exclude dirs
    if any(part.lower() in exclude_dirs for part in parts):
        return True

    # Check gitignore
    if gitignore_filter:
        rel_path = str(path)
        if gitignore_filter.is_ignored(rel_path):
            return True

    return False


def should_exclude_file(
    filename: str, 
    exclude_files: Set[str], 
    rel_path: Optional[str] = None,
    gitignore_filter: Optional[GitIgnoreFilter] = None
) -> bool:
    filename_lower = filename.lower()
    
    # Check default exclude files
    excluded_by_default = any(
        filename_lower == pattern.lower()
        or (
            pattern.startswith("*.")
            and filename_lower.endswith(pattern[2:].lower())
        )
        for pattern in exclude_files
    )
    if excluded_by_default:
        return True

    # Check gitignore
    if gitignore_filter and rel_path:
        if gitignore_filter.is_ignored(rel_path):
            return True

    return False
