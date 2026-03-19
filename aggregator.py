import os
import sys
from typing import Dict, List, Set
from pathlib import Path

# Ensure current directory is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from constants import MAX_FILE_SIZE
from detector import detect_project_tech, get_extensions_by_tech
from filters import (
    get_essential_files,
    get_exclude_patterns,
    should_exclude_path,
    should_exclude_file,
    get_ai_root_patterns,
    GitIgnoreFilter,
)

from tree_generator import generate_directory_tree


def aggregate_code(project_path: str, text: Dict[str, str], include_text: bool = False) -> bool:
    """Main function to aggregate project source code"""
    if not os.path.isdir(project_path):
        print(text["not_found"].format(path=project_path))
        return False

    print(text["analyzing"] + project_path)
    print(text["scanning"])

    # Detect tech
    detected_techs: List[str] = detect_project_tech(project_path)
    if detected_techs:
        print(text["tech_detected"] + ", ".join(detected_techs))
    else:
        print(text["no_tech"])

    target_extensions: Set[str] = get_extensions_by_tech(detected_techs)
    
    # ✅ Thêm .txt và .md nếu bật cờ
    if include_text:
        target_extensions.update({".txt", ".md"})

    get_essential_files()
    exclude_dirs, exclude_files = get_exclude_patterns()
    gitignore_filter = GitIgnoreFilter(project_path)

    print(text["included_ext"] + ", ".join(sorted(target_extensions)))

    content_lines: List[str] = []
    content_lines.append("# " + "=" * 50)
    content_lines.append(f"# {text['ai_context']}")
    content_lines.append("# " + "=" * 50)
    content_lines.append(f"# {text['project_path_label']}: {os.path.abspath(project_path)}")
    content_lines.append(
        f"# {text['tech_label']}: {', '.join(detected_techs) if detected_techs else 'Unknown'}"
    )
    content_lines.append("# " + "=" * 50)
    content_lines.append("")

    print(text["generating_tree"])
    content_lines.append("## DIRECTORY STRUCTURE")
    content_lines.append("```")
    content_lines.append(generate_directory_tree(project_path, exclude_dirs, exclude_files, gitignore_filter))
    content_lines.append("```")
    content_lines.append("")

    print(text["processing_files"])
    content_lines.append("## FILE CONTENTS")
    content_lines.append("")

    processed_files_sizes: List[int] = []

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [
            d for d in dirs
            if not should_exclude_path(os.path.join(root, d), exclude_dirs, gitignore_filter)
        ]

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_path)

            if should_exclude_path(rel_path, exclude_dirs, gitignore_filter) or \
               should_exclude_file(file, exclude_files, rel_path, gitignore_filter):
                continue

            file_ext = Path(file).suffix.lower()
            
            # ✅ Luôn bao gồm file HD dành cho AI ở ROOT
            is_ai_root = (root == project_path) and (file.lower() in {p.lower() for p in get_ai_root_patterns()})
            
            is_target_ext = file_ext in target_extensions or is_ai_root
            if not is_target_ext:
                continue



            try:
                file_size = os.path.getsize(file_path)
                if file_size > MAX_FILE_SIZE:
                    print(
                        text["skip_large"].format(
                            file=rel_path, size=file_size, limit=MAX_FILE_SIZE
                        )
                    )
                    continue

                print(text["processing"].format(file=rel_path))
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_content = f.read()

                # Use dynamic fencing to handle nested backticks
                fence = "```"
                while fence in file_content:
                    fence += "`"

                content_lines.append(f"### {rel_path}")
                content_lines.append(fence + (file_ext[1:] if file_ext else ""))
                content_lines.append(file_content)
                content_lines.append(fence)
                content_lines.append("")

                processed_files_sizes.append(len(file_content))

            except Exception as e:
                content_lines.append(f"### {rel_path}")
                content_lines.append(f"```\n# Error reading file: {str(e)}\n```")
                content_lines.append("")

    output_path = os.path.join(project_path, "project_codebase.md")
    final_content = "\n".join(content_lines)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        with open(output_path, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)

        print("")
        print(text["success"] + output_path)
        print("")
        print(text["summary"])
        file_count = len(processed_files_sizes)
        total_size = sum(processed_files_sizes)
        print(text["file_count"].format(count=file_count))
        print(text["size"].format(size=len(final_content), kb=total_size >> 10))
        print(text["line_count"].format(lines=line_count))
        print(text["sample_prompt"])
        return True

    except Exception as e:
        print(text["write_error"].format(error=str(e)))
        return False
