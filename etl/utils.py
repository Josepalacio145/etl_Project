import shutil
from pathlib import Path
from etl.logger import get_logger

logger = get_logger(__name__)

def move_file_to_processed(file_path: Path, processed_dir: str = "data/processed"):
    processed_dir = Path(processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    destination = processed_dir / file_path.name
    try:
        shutil.move(str(file_path), str(destination))
        logger.info(f"Archivo {file_path.name} movido a {destination}")
    except Exception as e:
        logger.error(f"No se pudo mover {file_path.name} a {processed_dir}: {e}", exc_info=True)