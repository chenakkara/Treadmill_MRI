# croping the image with manual box selection 
# input - image
# output - cropped image, crop box coordinates

import cv2
import matplotlib.pyplot as plt

def crop_frame(frame):
    global box    
    image = frame    
    # Create a callback function for mouse events
    box = []
    drawing = False
    def draw_rectangle(event, x, y, flags, param):
        global drawing,box    
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            box = [(x, y)]
                                   
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            box.append((x, y))
            cv2.rectangle(image, box[0], box[1], (0, 255, 0), 2)
            cv2.imshow("crop the image", image)            
    # Create a window and bind the draw_rectangle function to mouse events
    cv2.imshow("crop the image", image)
    cv2.setMouseCallback("crop the image", draw_rectangle)
          
    # Wait for the user to draw a box and press 'c' to crop the image
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            if len(box) == 2:
                # Crop the selected region            
                cropped_image = image[box[0][1]:box[1][1], box[0][0]:box[1][0]]                                
                cv2.imshow("Cropped Image", cropped_image)
                cv2.waitKey(0)
                break
        elif key == 27:  # Press 'Esc' to exit without cropping
            break    
    # Release all windows
    cv2.destroyAllWindows()
    return cropped_image, box

