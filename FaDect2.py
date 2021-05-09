import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2

class Window(object):
    
    def __init__(self):
        self.top = tk.Tk()
        self.top.title('FaDect2')
        self.frames_list = []
        self.buttons_list = []
        self.entries_list = []
        self.labels_list = []

    def init_frame_grid(self, frame, text = 'Frame', row = 0, column = 0, rowspan = 1, columnspan = 1):
        self.frames_list.append([tk.LabelFrame(frame, text = text), (row, column), (rowspan, columnspan)])

    def pack_frames_grid(self):
        for frame, position, spans in self.frames_list:
            frame.grid(row = position[0], column = position[1], rowspan = spans[0], columnspan = spans[1])

    def init_buttons_grid(self, frame, text = 'Frame', command = None, row = 0, column = 0, rowspan = 1, columnspan = 1):
        self.buttons_list.append([tk.Button(frame, text = text, command = command), (row, column), (rowspan, columnspan)])

    def pack_buttons_grid(self):
        for button, position, spans in self.buttons_list:
            button.grid(row = position[0], column = position[1], rowspan = spans[0], columnspan = spans[1])

    def init_entries_grid(self, frame, value, row = 0, column = 0, rowspan = 1, columnspan = 1):
        temp = tk.Entry(frame)
        temp.insert(tk.END, value)
        self.entries_list.append([temp, (row, column), (rowspan, columnspan)])

    def pack_entries_grid(self):
        for entry, position, spans in self.entries_list:
            entry.grid(row = position[0], column = position[1], rowspan = spans[0], columnspan = spans[1])

    def init_labels_grid(self, frame, text = 'Frame', row = 0, column = 0, rowspan = 1, columnspan = 1):
        self.labels_list.append([tk.Label(frame, text = text), (row, column), (rowspan, columnspan)])

    def pack_labels_grid(self):
        for label, position, spans in self.labels_list:
            label.grid(row = position[0], column = position[1], rowspan = spans[0], columnspan = spans[1])


class Window_Variable(object):

    def __init__(self, window):
        self.image_buffer = None
        self.image_path = None
        self.image_panel = None
        self.scale_factor = 1.1
        self.min_neighbors = 4
        self.face_cascade = cv2.CascadeClassifier('Haars\haarcascade_frontalface_default.xml')
        self.window = window
        self.init_gui()
    
    # wybór zdjęcia
    def select_image(self):

        self.image_path = tk.filedialog.askopenfilename()

        if(len(self.image_path) > 0):
            self.update_image()

    def update_image(self):

        self.scale_factor = float(self.window.entries_list[0][0].get())
        self.min_neighbors = int(self.window.entries_list[1][0].get())

        self.image_buffer = cv2.imdecode(np.fromfile(self.image_path, np.uint8), cv2.IMREAD_UNCHANGED)
        im_size = (500, 500)
        scale = max(self.image_buffer.shape[0]/im_size[0], self.image_buffer.shape[1]/im_size[1])

        if self.image_buffer is not None:

            gray = cv2.cvtColor(self.image_buffer, cv2.COLOR_BGR2GRAY)

            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(gray, self.scale_factor, self.min_neighbors)

                for (x, y, w, h) in faces:
                    cv2.rectangle(self.image_buffer, (x, y), (x+w, y+h), (255, 0, 0), int(2*scale))

            dsize = (int(self.image_buffer.shape[1]/scale), int(self.image_buffer.shape[0]/scale))
            self.image_buffer = cv2.resize(self.image_buffer, dsize)

            image = cv2.cvtColor(self.image_buffer, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

        if self.image_panel is None:
            self.image_panel = tk.Label(self.window.frames_list[0][0], image = image)
            self.image_panel.image = image
            self.image_panel.pack(padx = 10, pady = 10)

        else:
            self.image_panel.configure(image = image)
            self.image_panel.image = image

    def run_window(self):
        self.window.top.mainloop()

    # tutaj odbywa się tworzenie i aranżowanie okienek
    def init_gui(self):
        self.window.init_frame_grid(self.window.top, text = 'Zdjęcie', row = 0, column = 0, rowspan = 2)
        self.window.init_frame_grid(self.window.top, text = 'Opcje', row = 0, column = 1)
        self.window.init_frame_grid(self.window.top, text = 'Wybierz', row = 1, column = 1)

        self.window.init_buttons_grid(self.window.frames_list[1][0], text = 'Odśwież', command = self.update_image, row = 2, column = 0, columnspan = 2)
        self.window.init_buttons_grid(self.window.frames_list[2][0], text = 'Wybierz Zdjęcie', command = self.select_image, row = 0, column = 0)

        self.window.init_entries_grid(self.window.frames_list[1][0], value = self.scale_factor, row = 0, column = 1)
        self.window.init_entries_grid(self.window.frames_list[1][0], value = self.min_neighbors, row = 1, column = 1)

        self.window.init_labels_grid(self.window.frames_list[1][0], text = 'scaleFactor', row = 0, column = 0)
        self.window.init_labels_grid(self.window.frames_list[1][0], text = 'minNeighbors', row = 1, column = 0)

        self.window.pack_frames_grid()
        self.window.pack_buttons_grid()
        self.window.pack_entries_grid()
        self.window.pack_labels_grid()
# ---------------------------------------------------------------------------------------------------------------
# zmienne
Root = Window()
Variables = Window_Variable(Root)
Variables.run_window()