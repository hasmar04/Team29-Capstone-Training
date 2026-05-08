import cv2
import os
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# === CONFIG ===
input_root = r"\Where\Your\Videos\Are"
output_folder = r"\Where\You\Want\To\Save\Frames"
frame_interval_seconds = 2
max_workers = 4

os.makedirs(output_folder, exist_ok=True)


def clean_name(name):
    name = name.lower()
    name = name.replace(" ", "-")
    name = re.sub(r"[^a-z0-9\-]", "", name)
    return name


def get_all_videos(root_folder):
    video_paths = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".mov"):
                video_paths.append(os.path.join(root, file))
    return video_paths


def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return (video_path, 0, "Failed")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0 or total_frames <= 0:
        cap.release()
        return (video_path, 0, "Invalid")

    step = max(1, int(fps * frame_interval_seconds))

    parent_folder = os.path.basename(os.path.dirname(video_path))
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    parent_clean = clean_name(parent_folder)
    video_clean = clean_name(video_name)

    saved_count = 0

    for frame_index in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if not ret:
            continue

        filename = f"{parent_clean}-{video_clean}-{saved_count + 1:05d}.jpg"
        filepath = os.path.join(output_folder, filename)

        cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        saved_count += 1

    cap.release()
    return (video_name, saved_count, "OK")


if __name__ == "__main__":
    video_paths = get_all_videos(input_root)
    print(f"Found {len(video_paths)} videos\n")

    total_frames_saved = 0
    results = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_frames, path) for path in video_paths]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing videos"):
            try:
                result = future.result()
                results.append(result)
                total_frames_saved += result[1]
            except Exception as e:
                print(f"Error: {e}")

    # === FINAL SUMMARY ===
    print("\n========== DONE ==========")
    print(f"Videos processed: {len(results)}")
    print(f"Total frames saved: {total_frames_saved}")

    failed = [r for r in results if r[2] != "OK"]
    if failed:
        print(f"Failures: {len(failed)}")
        for f in failed:
            print(f" - {f[0]} ({f[2]})")
    else:
        print("All videos processed successfully")

    print(f"\nFrames saved to: {output_folder}")