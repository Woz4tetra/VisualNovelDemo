from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
ASSETS = PROJECT_ROOT / "assets"
STORIES = PROJECT_ROOT / "stories"


def load_path_cache(root: Path, extensions: tuple[str, ...]) -> dict[str, str]:
    files = {}
    for path, dirnames, filenames in root.walk():
        for filename in filenames:
            filename_lower = filename.lower()
            if not any(filename_lower.endswith(ext) for ext in extensions):
                continue
            filepath = path / filename
            key = str(path.relative_to(root) / filepath.stem)
            files[key] = filepath
    return files
