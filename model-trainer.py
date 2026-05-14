#######################################

  #PASTE YOUR ROBOFLOW SNIPPET HERE#

#######################################

from ultralytics import YOLO
model = YOLO("yolo26m.pt")

model.train(
    data=f"{dataset.location}/data.yaml",
    epochs=100,
    imgsz=640,
    batch=16
)
