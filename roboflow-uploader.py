from roboflow import Roboflow
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

API_KEY = "YOUR_API_KEY"

WORKSPACE = "YOUR WORKSPACE"
PROJECT = "YOUR PROJECT"

INPUT_ROOT = r"D:\your\images"

rf = Roboflow(api_key=API_KEY)

project = rf.workspace(WORKSPACE).project(PROJECT)

image_extensions = [".jpg", ".jpeg", ".png"]

image_paths = []

for ext in image_extensions:
    image_paths.extend(Path(INPUT_ROOT).rglob(f"*{ext}"))

print(f"Found {len(image_paths)} images")


def upload_image(image_path):
    try:
        project.upload(
            image_path=str(image_path),
            batch_name="bulk_upload"
        )

        print(f"Uploaded: {image_path.name}")

    except Exception as e:
        print(f"Failed: {image_path.name}")
        print(e)


with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(upload_image, image_paths)

print("Done")
