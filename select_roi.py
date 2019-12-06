import cv2
import camera

with camera.GetCamera(0) as cam:
    for i in range(100):
        cam.capture()
    IMAGE = cam.capture()


def convert_roi_to_bbox(roi):
    return (roi[1], roi[1] + roi[3], roi[0], roi[0] + roi[2])


def main():
    ROIs = cv2.selectROIs(
        'Select -> <Enter> -> Select -> <Enter> -> <Esc>', IMAGE, fromCenter=False)  # (xmin, ymin, w, h)
    ROI_bboxes = list(map(convert_roi_to_bbox, ROIs))

    [print(f'Box {i}: {bbox}') for i, bbox in enumerate(ROI_bboxes)]


if __name__ == "__main__":
    main()
