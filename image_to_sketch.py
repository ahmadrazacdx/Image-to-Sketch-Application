# Image To Sketch by @ Ahmad Raza
import os
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


def is_valid_image_extension(filename):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)
    
def get_input_image_path():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path and is_valid_image_extension(file_path):
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, file_path)
    else:
        messagebox.showerror("Error", "Invalid image file selected!")
        
def get_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, folder_path)
        
def pencil_sketch(input_image_path, output_folder_path, kernel_size=(11, 11), sigma=0):
    try:
        image = cv2.imread(input_image_path)
        if image is None:
            raise ValueError("Error: Unable to read the input image. Please check the file path.")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted_gray_image = 255 - gray_image
        blurred_image = cv2.GaussianBlur(inverted_gray_image, kernel_size, sigmaX=sigma, sigmaY=sigma)
        inverted_blurred_image = 255 - blurred_image
        pencil_sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

        name = 1
        file_extension = os.path.splitext(input_image_path)[-1]
        output_sketch_path = os.path.join(output_folder_path, f"sketch_{str(name)}" + file_extension)
        name += 1

        cv2.imwrite(output_sketch_path, pencil_sketch)
        messagebox.showinfo("Success", "Pencil sketch saved as: " + output_sketch_path)

        input_path_entry.delete(0, tk.END)
        output_path_entry.delete(0, tk.END)
        choice_var.set("2")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def generate_sketch():
    input_image_path = input_path_entry.get()
    output_sketch_path = output_path_entry.get()
    try:
        choice = int(choice_var.get())
        if choice == 1:
            kernel_size = (7, 7)
        elif choice == 2:
            kernel_size = (11, 11)
        elif choice == 3:
            kernel_size = (17, 17)
        elif choice == 4:
            kernel_size = (21, 21)
        else:
            raise ValueError("Invalid choice. Please select a valid option (1/2/3).")
        pencil_sketch(input_image_path, output_sketch_path, kernel_size=kernel_size)
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred: " + str(e))

root = tk.Tk()
root.title("Sketch Generator")
root.geometry('460x205')
root.resizable(False, False)
root.configure(bg='#828282')

frame = tk.Frame(root,bg='#828282')
frame.pack()

# Selection Frame
selection_frame = tk.LabelFrame(frame, text="Selection",bg='#828282', fg='#000000')
selection_frame.grid(row=0, column=0, padx=20, pady=10)

input_path_label = tk.Label(selection_frame, text="Input Image",bg='#828282', fg='#000000')
input_path_label.grid(row=0, column=0, padx=10, pady=5)

input_path_entry = tk.Entry(selection_frame, width=35)
input_path_entry.grid(row=0, column=1, padx=10, pady=5)

browse_input_button = tk.Button(selection_frame, text="Browse",bg='#828282', command=get_input_image_path, fg='#000000', width=7, bd=1)
browse_input_button.grid(row=0, column=2, padx=10, pady=5)

output_path_label = tk.Label(selection_frame, text="Output Folder",bg='#828282', fg='#000000')
output_path_label.grid(row=1, column=0, padx=5, pady=5)

output_path_entry = tk.Entry(selection_frame, width=35)
output_path_entry.grid(row=1, column=1, padx=10, pady=5)

browse_output_button = tk.Button(selection_frame, text="Browse", bg='#828282', command=get_output_folder, fg='#000000',width=7, bd=1)
browse_output_button.grid(row=1, column=2, padx=10, pady=5)

# Levels Frame
level_frame = tk.LabelFrame(frame, text="Levels", bg='#828282', fg='#000000')
level_frame.grid(row=1, column=0, padx=20, pady=0, sticky='ew')

choice_var = tk.IntVar()
choice_var.set(2)

small_radio = tk.Radiobutton(level_frame, text="Small", variable=choice_var, value=1,bg='#828282' , fg='#000000')
normal_radio = tk.Radiobutton(level_frame, text="Normal", variable=choice_var, value=2, bg='#828282', fg='#000000')
medium_radio = tk.Radiobutton(level_frame, text="Medium", variable=choice_var, value=3,bg='#828282', fg='#000000')
best_radio = tk.Radiobutton(level_frame, text="Best", variable=choice_var, value=4,bg='#828282' , fg='#000000')
small_radio.grid(row=0,column=0)
normal_radio.grid(row=0, column=1)
medium_radio.grid(row=0, column=2)
best_radio.grid(row=0, column=3)

button = tk.Button(root, text="Generate", command=generate_sketch, width=10,bg='#828282', fg='#000000', bd=1)
button.pack(padx=10, pady=10)

root.mainloop()
