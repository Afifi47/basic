import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from ultralytics import YOLO
import numpy as np

# Load YOLOv8 model
model = YOLO('C:/Users/Lenovo Legion 5 Pro/Desktop/Degree/PSM/PSM 1/Baru Baru/Best_PT_File/best.pt')

class_labels = ['immature', 'mature']  # Updated class labels

# Function to open a file dialog and select an image
def upload_image():
    global img_path
    img_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if img_path:
        # Display the selected image
        display_image(img_path)
        # Predict and display bounding box
        predict_image()

# Function to display the image in the GUI
def display_image(img_path):
    img = Image.open(img_path)
    img = img.resize((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    
    # Update the label with the new image
    image_label.config(image=img_tk)
    image_label.image = img_tk

def draw_bounding_boxes(image, results, avg_colors):
    draw = ImageDraw.Draw(image)
    font_size = max(10, int(min(image.size) / 20))  # Adjust font size based on image size
    font = ImageFont.truetype("arial.ttf", font_size)
    maize_counter = 1
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            box = box.tolist()  # Get bounding box coordinates
            label = class_labels[int(cls)]  # Get class label
            color = "green" if label == "mature" else "red"
            draw.rectangle(box, outline=color, width=3)
            draw.text((box[0], box[1]), f"{label} {maize_counter}", fill=color, font=font)
            draw.text((box[0], box[1] + font_size), f"RGB: {avg_colors[maize_counter-1]}", fill=color, font=font)
            maize_counter += 1
    return image

def analyze_color(image, boxes):
    avg_colors = []
    np_image = np.array(image)
    
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.tolist())
        roi = np_image[y1:y2, x1:x2]
        
        # Calculate average RGB values for the region of interest (ROI)
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        
        avg_colors.append(avg_color)
    
    return avg_colors

def predict_image():
    results = model(img_path)
    if results:
        img = Image.open(img_path)
        
        # Analyze color and get average RGB values for each detected maize
        boxes = [box for result in results for box in result.boxes.xyxy]
        avg_colors = analyze_color(img, boxes)
        
        img_with_boxes = draw_bounding_boxes(img, results, avg_colors)
        img_with_boxes = img_with_boxes.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img_with_boxes)
        
        # Update the label with the new image with bounding boxes and labels
        image_label.config(image=img_tk)
        image_label.image = img_tk
        
        # Display RGB values in the result label for each detected maize
        rgb_info = "\n".join([f"Maize {i+1} RGB: {avg_colors[i]}" for i in range(len(avg_colors))])
        result_label.config(text=rgb_info)

def on_closing():
    root.quit()  # Stop the Tkinter event loop
    root.destroy()  # Close the window and destroy all widgets

# Create the main window
root = tk.Tk()
root.title("Colorimetric-based Maturity Assessment of Blue Maize")

root.geometry("500x500")
root.protocol("WM_DELETE_WINDOW", on_closing)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create and place the buttons and labels
upload_button = tk.Button(button_frame, text="Upload Image", command=upload_image, height=2, width=15)
upload_button.pack(side='left', padx=(20, 30))

image_label = tk.Label(root)
image_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
result_label.pack(pady=20)

# Start the GUI event loop
root.mainloop()
