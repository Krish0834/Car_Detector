import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from detector import model, is_blue_car

def process_image(path):
    img = cv2.imread(path)
    results = model(img)
    detected = results.pandas().xyxy[0]
    
    people_count = 0
    total_cars = 0
    blue_cars = 0

    for index, row in detected.iterrows():
        cls = row['name']
        x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])

        if cls == 'car':
            total_cars += 1
            roi = img[y1:y2, x1:x2]

            if is_blue_car(roi):
                blue_cars += 1
                color = (0, 0, 255)  # red for blue cars
            else:
                color = (255, 0, 0)  # blue for other cars

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        elif cls == 'person':
            people_count += 1
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display counts on image
    cv2.putText(img, f'People: {people_count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f'Total Cars: {total_cars}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, f'Blue Cars: {blue_cars}', (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return img

 

def open_image():
    path = filedialog.askopenfilename()
    img = process_image(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

root = tk.Tk()
root.title("Car Color Detector")

btn = tk.Button(root, text="Upload Image", command=open_image)
btn.pack()

label = tk.Label(root)
label.pack()

root.mainloop()
