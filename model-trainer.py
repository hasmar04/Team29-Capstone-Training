#######################################

  #PASTE YOUR ROBOFLOW SNIPPET HERE#

#######################################

from ultralytics import YOLO
# keep your model
model = YOLO("yolo26m.pt")

model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)
