!pip install roboflow ultralytics

from roboflow import Roboflow
from ultralytics import YOLO

# init roboflow
rf = Roboflow(api_key="INSERT YOUR API KEY")

project = rf.workspace("WORKSPACE").project("PROJECT")

dataset = project.version(1).download("yolov8") 

print(dataset.location)

# keep your model
model = YOLO("yolo26m.pt")

model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)
