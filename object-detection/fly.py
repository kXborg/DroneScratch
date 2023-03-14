import cv2
import time
from time import sleep 
import keyboard as key
from detection import *
from djitellopy import tello 
from ultralytics import YOLO
from datetime import datetime


def controls():
    lr, fb, ud, rot = 0, 0, 0, 0
    speed = 50 

    if key.getKey("LEFT"): lr = -speed
    if key.getKey("RIGHT"): lr = speed

    if key.getKey("UP"): fb = speed 
    if key.getKey("DOWN"): fb = -speed 

    if key.getKey("w"): ud = speed 
    if key.getKey("s"): ud = -speed

    if key.getKey("a"): rot = -speed 
    if key.getKey("d"): rot = speed

    if key.getKey("t"): drone.takeoff()
    if key.getKey("l"): drone.land()

    return [lr, fb, ud, rot]

if __name__ == "__main__":
    # Initializations.
    key.init()
    drone = tello.Tello()
    # Start the drone.
    drone.connect()
    print(drone.get_battery())
    # Start video stream.
    drone.streamon()
    print('Video stream started.')

    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")

    # Create the video writer.
    out = cv2.VideoWriter(f"video-{date_time}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 25, (960, 720))

    # Load model.
    model = YOLO('yolov8n.pt')

    while True:
        # Acquire control speeds.
        vals = controls()
        # Send control signal.
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

        img = drone.get_frame_read().frame
        t1 = time.time()
        det_img = draw_predictions(img.copy(), model)
        t2 = time.time()
        det_time = t2 - t1
        fps = int(1/det_time)
        print(img.shape)
        cv2.putText(det_img, f"FPS : {fps}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

        # Display.
        cv2.imshow('Stream', det_img)
        out.write(det_img)
        wait = cv2.waitKey(1)

        if wait == ord('q'):
            print('Program Terminated')
            print('\n Thanks for flying Tello.')
            break

    # Release the video writer.
    out.release()
