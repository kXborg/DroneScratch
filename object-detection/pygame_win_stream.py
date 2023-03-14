import cv2
import time
import pygame
from time import sleep 
from detection import *
from djitellopy import tello 
from ultralytics import YOLO
from datetime import datetime


def controls():
    lr, fb, ud, rot = 0, 0, 0, 0
    speed = 50
    stop = False

    if getKey("LEFT"): lr = -speed
    if getKey("RIGHT"): lr = speed

    if getKey("UP"): fb = speed 
    if getKey("DOWN"): fb = -speed 

    if getKey("w"): ud = speed 
    if getKey("s"): ud = -speed

    if getKey("a"): rot = -speed 
    if getKey("d"): rot = speed

    if getKey("t"): drone.takeoff()
    if getKey("l"): drone.land()

    if getKey("q"): stop = True

    return stop, [lr, fb, ud, rot]


def getKey(keyname):
    ans = False
    for event in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyname))
    if keyInput[myKey]:
        ans = True
    
    # pygame.display.update()
    return ans


if __name__ == "__main__":
    # Initializations.
    pygame.init()
    screen = pygame.display.set_mode((960*2, 720*2))
    pygame.display.set_caption("Video Stream")

    drone = tello.Tello()

    # Start the drone.
    drone.connect()
    print('Initial Capacity: ', drone.get_battery())

    # Start video stream.
    drone.streamon()
    print('Video stream started.')

    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y-%H-%M-%S")

    # Create the video writer.
    out = cv2.VideoWriter(f"video-{date_time}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (960, 720))

    # Load model.
    model = YOLO('yolov8n.pt')

    
    while True:
        # Acquire control speeds.
        stop_event, vals = controls()
        # Send control signal.
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

        img = drone.get_frame_read().frame

        battery_perc = drone.get_battery()

        if img is not None:
            t1 = time.time()
            det_img = draw_predictions(img.copy(), model)
            t2 = time.time()
            det_time = t2 - t1
            fps = int(1/det_time)
            print(img.shape)
            cv2.putText(det_img, f"FPS : {fps}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
            cv2.putText(det_img, f"Battery: {battery_perc}", (740, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

            # Display.
            out.write(det_img)

            det_img = cv2.resize(det_img, None, fx=2, fy=2)

            py_det_img = cv2.cvtColor(det_img, cv2.COLOR_BGR2RGB)
            py_det_img = cv2.rotate(py_det_img, cv2.ROTATE_90_CLOCKWISE)
            py_det_img = cv2.flip(py_det_img, 1)
            py_det_img = pygame.surfarray.make_surface(py_det_img)
            screen.blit(py_det_img, (0,0))
            pygame.display.update()

            if stop_event:
                print('Program terminated. \n Thanks for flying Tello.')
                break

    # Release the video writer.
    out.release()
