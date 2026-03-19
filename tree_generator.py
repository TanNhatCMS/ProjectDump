import os
from typing import List, Optional, Set
from filters import should_exclude_path, should_exclude_file, GitIgnoreFilter


def generate_directory_tree(
    project_path: str, 
    exclude_dirs: Set[str], 
    exclude_files: Set[str],
    gitignore_filter: Optional[GitIgnoreFilter] = None
) -> str:
    tree_lines: List[str] = []
    project_name: str = os.path.basename(project_path.rstrip(os.sep))
    tree_lines.append(f"{project_name}/")

    def add_directory_content(current_path: str, prefix: str = "") -> None:
        try:
            items: List[str] = sorted(os.listdir(current_path))
            dirs: List[str] = [
                item
                for item in items
                if os.path.isdir(os.path.join(current_path, item))
            ]
            files: List[str] = [
                item
                for item in items
                if os.path.isfile(os.path.join(current_path, item))
            ]

            # Hiển thị thư mục
            for i, dirname in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0

                # Kiểm tra xem có phải thư mục bị loại bỏ không
                rel_dir_path = os.path.relpath(os.path.join(current_path, dirname), project_path)
                if should_exclude_path(rel_dir_path, exclude_dirs, gitignore_filter):
                    tree_lines.append(
                        f"{prefix}{'└── ' if is_last_dir else '├── '}{dirname}/"
                    )
                    continue  # Không duyệt vào bên trong thư mục bị loại bỏ
                else:
                    tree_lines.append(
                        f"{prefix}{'└── ' if is_last_dir else '├── '}{dirname}/"
                    )
                    next_prefix = prefix + ("    " if is_last_dir else "│   ")
                    add_directory_content(
                        os.path.join(current_path, dirname), next_prefix
                    )

            # Hiển thị files
            # Cần lọc danh sách files trước để biết file nào là cuối cùng thực sự
            filtered_files = []
            for filename in files:
                rel_file_path = os.path.relpath(os.path.join(current_path, filename), project_path)
                if not should_exclude_file(filename, exclude_files, rel_file_path, gitignore_filter):
                    filtered_files.append(filename)

            for i, filename in enumerate(filtered_files):
                is_last = i == len(filtered_files) - 1
                tree_lines.append(
                    f"{prefix}{'└── ' if is_last else '├── '}{filename}"
                )

        except PermissionError:
            tree_lines.append(f"{prefix}├── [Permission Denied]")

    add_directory_content(project_path)
    return "\n".join(tree_lines)
