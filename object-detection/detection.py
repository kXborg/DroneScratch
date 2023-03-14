import cv2
import numpy as np 
from ultralytics import YOLO
import colorsys
import random


def get_colors(num: int = 1) -> list:

    random.seed(0)
    hsv_tuples = [(x/num, random.uniform(0.4, 1.0), random.uniform(0.4, 1.0)) for x in range(num)]

    rgb_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    rgb_tuples = list(map(lambda x: (x[0]*255, x[1]*255, x[2]*255), rgb_tuples))

    return rgb_tuples


def draw_predictions(img, model):
    results = model.predict(source=img)
    results = results[0].cpu().numpy()

    COLORS = get_colors(80)
    

    FONT_SIZE = int((img.shape[0]*img.shape[1])/(3*(10)**6))

    if FONT_SIZE < 1: FONT_SIZE = 1
    
    print(img.shape[0]*img.shape[1])
    print(f"Font size : {FONT_SIZE}")

    with open('names.txt', 'r') as f:
        lines = f.readlines()
        coco_names = []
        for line in lines:
            name = line.replace("\n","")
            coco_names.append(name)
    # print(coco_names)
    boxes = results.boxes

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        print(x1, y1, x2, y2)

        cls_id = int(box.cls.tolist()[0])

        # Define random color.
        blue = random.randrange(0, 255, 10)
        green = random.randrange(0, 255, 10)
        red = random.randrange(0, 255, 10)

        COLOR = COLORS[cls_id]
        class_name = coco_names[cls_id]
        print(class_name)

        (label_width, label_height), baseline = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_COMPLEX, 2, 2)

        cv2.putText(img, class_name, (x1, y1 - int(0.2*label_height)), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, COLOR, 1)
        cv2.rectangle(img, (x1, y1), (x2, y2), COLOR, thickness=2, lineType=cv2.LINE_AA)

    return img


if __name__ == '__main__':
    image = cv2.imread('test-img.jpg')
    model = YOLO('yolov8l.pt')
    out_img = draw_predictions(image, model)
    cv2.imshow('Output', out_img)
    key = cv2.waitKey(0)