import camera
import cv2

N_WARMUP = 100
TOTAL_PHOTOS = 200

with camera.GetCamera() as cam:
    cam.warmup(N_WARMUP)
    [cv2.imwrite(f'im_{n}.png', cam.capture()) for n in range(TOTAL_PHOTOS)]
