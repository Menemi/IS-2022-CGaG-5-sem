from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox
from lab1.managers.pgm_manager import PgmManager
from lab1.managers.ppm_manager import PpmManager
from exceptions import IncorrectFileFormatError
from PIL import Image, ImageTk
from lab2.color_space_converter import ColorSpaceConverter
import numpy as np
from copy import deepcopy
from lab3.GammaConverter import GammaConverter
from lab5.Ditherer import Ditherer
from lab6.ResizeConverter import ResizeConverter
from lab7.PngManager import PngManager


class Interface:
    def __init__(self):
        self.figure = None
        self.window = None
        self.txt = None
        self.txt2 = None
        self.color_space = "RGB"
        self.data = None
        self.usage_frame = None
        self.image_frame = None
        self.canvas_img = None
        self.manager = None

    def show(self, image_frame):
        def selected_channel(event):
            ch = channel.get()
            new_data = deepcopy(self.data)
            if ch == "1":
                new_data[:, :, 1] = new_data[:, :, 2] = 0
            elif ch == "2":
                new_data[:, :, 0] = new_data[:, :, 2] = 0
            elif ch == "3":
                new_data[:, :, 1] = new_data[:, :, 0] = 0

            new_img = Image.fromarray((new_data * 255).astype(np.uint8), current)
            new_imgkt = ImageTk.PhotoImage(new_img)

            canvas.create_image(0, 0, anchor=NW, image=new_imgkt)
            canvas.image = new_imgkt

        def show_with_gamma():
            img_gamma = Image.fromarray((converter.data_with_gamma * 255).astype(np.uint8), current)
            imgkt_gamma = ImageTk.PhotoImage(img_gamma)
            canvas.create_image(0, 0, anchor=NW, image=imgkt_gamma)
            canvas.image = imgkt_gamma

            if isinstance(self.manager, PngManager):
                self.manager.gamma = converter.gamma

        def show_with_dithering(event):
            method = dithering.get()

            if method == "normal":
                img = Image.fromarray((self.data * 255).astype(np.uint8))
                imgkt = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor=NW, image=imgkt)
                canvas.image = imgkt
                return

            byte = 8 if bitness.get() == "" else int(bitness.get())

            img_dithering = Image.fromarray(
                (Ditherer.__getattribute__(ditherer, method)(self.data, byte) * 255).astype(np.uint8))
            imgkt_dithering = ImageTk.PhotoImage(img_dithering)

            canvas.create_image(0, 0, anchor=NW, image=imgkt_dithering)
            canvas.image = imgkt_dithering

        def resize(event):
            new_data = deepcopy(self.data)
            method = resizer_box.get()
            height, width = resizer_txt.get().split()

            if method == "bc_splines":
                b, c = spline_txt.get().split()
                imgkt_resized = ImageTk.PhotoImage(Image.fromarray(
                    (ResizeConverter.bc_splines(new_data, int(height), int(width), float(b), float(c)) * 255).astype(
                        np.uint8)
                ))
            else:
                imgkt_resized = ImageTk.PhotoImage(Image.fromarray(
                    (getattr(ResizeConverter, method)(new_data, int(height), int(width)) * 255).astype(np.uint8)
                ))

            self.canvas_img = canvas.create_image(0, 0, anchor=NW, image=imgkt_resized)
            canvas.image = imgkt_resized

        def move_picture():
            x, y = list(map(int, moving_txt.get().split()))
            canvas.move(self.canvas_img, int(x), int(y))

        ditherer = Ditherer()
        current = None
        if self.color_space == "RGB":
            current = "RGB"
        elif self.color_space in ["HSV", "HSL"]:
            current = "HSV"
        elif self.color_space in ["YCbCr.601", "YCbCr.709", "YCoCg"]:
            current = "YCbCr"
        elif self.color_space == "CMYK":
            current = "CMYK"

        img = Image.fromarray((self.data * 255).astype(np.uint8))
        imgkt = ImageTk.PhotoImage(img)

        canvas = Canvas(image_frame, width=800, height=800)
        canvas.grid(column=0, row=0)

        channel_txt = Label(self.usage_frame, text="Select channel to show")
        channel_txt.grid(column=3, row=1)

        channel = Combobox(self.usage_frame,
                           values=["ALL", "1", "2", "3"],
                           state="readonly")
        channel.bind("<<ComboboxSelected>>", selected_channel)
        channel.grid(column=4, row=1, sticky=NW)

        converter = GammaConverter(self.data)

        gamma_lbl = Label(self.usage_frame, text="Set gamma")
        gamma_lbl.grid(column=5, row=0)

        gamma_txt = Entry(self.usage_frame)
        gamma_txt.grid(column=6, row=0)

        convert_btn = Button(self.usage_frame, text="Convert", command=lambda: converter.convert(gamma_txt.get()))
        convert_btn.grid(column=5, row=1)

        show_btn = Button(self.usage_frame, text="Show", command=show_with_gamma)
        show_btn.grid(column=6, row=1)

        dither_lbl = Label(self.usage_frame, text="Choose dithering")
        dither_lbl.grid(column=7, row=0)

        dithering = Combobox(self.usage_frame,
                             values=["normal", "random", "ordered", "atkinson", "floyd_steinberg"],
                             state="readonly")
        dithering.bind("<<ComboboxSelected>>", show_with_dithering)
        dithering.grid(column=8, row=0, sticky=NW)

        bitness_lbl = Label(self.usage_frame, text="Choose bitness")
        bitness_lbl.grid(column=7, row=1)

        bitness = Combobox(self.usage_frame,
                           values=["1", "2", "3", "4", "5", "6", "7", "8"],
                           state="readonly")
        bitness.bind("<<ComboboxSelected>>", show_with_dithering)
        bitness.grid(column=8, row=1, sticky=NW)

        resizer_lbl = Label(self.usage_frame, text="Choose resize algorithm")
        resizer_lbl.grid(column=0, row=2)

        resizer_box = Combobox(self.usage_frame,
                               values=["closest_neighbour", "bilinear", "lanczos", "bc_splines"],
                               state="readonly")
        resizer_box.bind("<<ComboboxSelected>>", resize)
        resizer_box.grid(column=1, row=2, sticky=NW)

        resizer_lbl2 = Label(self.usage_frame, text="Set new height and width")
        resizer_lbl2.grid(column=2, row=2)

        resizer_txt = Entry(self.usage_frame)
        resizer_txt.grid(column=3, row=2)

        moving_lbl = Label(self.usage_frame, text="Move on (x y)")
        moving_lbl.grid(column=4, row=2)

        moving_txt = Entry(self.usage_frame)
        moving_txt.grid(column=5, row=2)

        moving_btn = Button(self.usage_frame, text="Move", command=move_picture)
        moving_btn.grid(column=6, row=2)

        spline_lbl = Label(self.usage_frame, text="Set B and C")
        spline_lbl.grid(column=7, row=2)

        spline_txt = Entry(self.usage_frame)
        spline_txt.grid(column=8, row=2)

        self.canvas_img = canvas.create_image(0, 0, anchor=NW, image=imgkt)
        canvas.image = imgkt

    def choose_function_to_save(self, frame):
        filename = self.txt2.get()

        if filename[-3:] == "pgm":
            self.save_pgm_on_click(frame)
        elif filename[-3:] == "ppm":
            self.save_ppm_on_click(frame)
        elif filename[-3:] == "ppm":
            self.save_png_on_click(frame)
        else:
            messagebox.showerror("Error", "Incorrect file format")

    def choose_function_to_read(self, frame):
        filename = self.txt.get()

        if len(filename) < 5:
            messagebox.showerror("Error", "Invalid input")
        elif filename[-3:] == "pgm":
            self.read_pgm_on_click(frame)
        elif filename[-3:] == "ppm":
            self.read_ppm_on_click(frame)
        elif filename[-3:] == "png":
            self.read_png_on_click(frame)
        else:
            messagebox.showerror("Error", "Incorrect file format")

    def read_pgm_on_click(self, image_frame):
        self.manager = PgmManager()
        filename = self.txt.get()
        self.txt.delete(0, len(filename))

        try:
            self.manager.read_p5(filename)
        except FileNotFoundError:
            messagebox.showerror("Error", "There is no file with this name")
            return
        except IncorrectFileFormatError:
            messagebox.showerror("Error", "This file has incorrect format")
        self.data = self.manager.data
        self.show(image_frame)

    def save_pgm_on_click(self, image_frame):
        self.manager = PgmManager()
        path_to_save = self.txt2.get()

        self.txt2.delete(0, len(path_to_save))

        self.manager.save_p5(self.data, path_to_save)

        self.show(image_frame)

    def read_ppm_on_click(self, image_frame):
        self.manager = PpmManager()
        filename = self.txt.get()
        self.txt.delete(0, len(filename))

        try:
            self.manager.read_p6(filename)
        except FileNotFoundError:
            messagebox.showerror("Error", "There is no file with this name")
            return
        except IncorrectFileFormatError:
            messagebox.showerror("Error", "This file has incorrect format")

        self.data = self.manager.data
        self.show(image_frame)

    def save_ppm_on_click(self, show_frame):
        self.manager = PpmManager()
        path_to_save = self.txt2.get()

        self.txt2.delete(0, len(path_to_save))

        self.manager.save_p6(self.data, path_to_save)

        self.show(show_frame)

    def read_png_on_click(self, image_frame):
        self.manager = PngManager()
        filename = self.txt.get()
        self.txt.delete(0, len(filename))

        try:
            self.manager.read(filename)
        except FileNotFoundError:
            messagebox.showerror("Error", "There is no file with this name")
            return
        except IncorrectFileFormatError:
            messagebox.showerror("Error", "This file has incorrect format")

        self.data = self.manager.data
        self.show(image_frame)

    def save_png_on_click(self, image_frame):
        self.manager = PngManager()
        path_to_save = self.txt2.get()

        self.txt2.delete(0, len(path_to_save))

        self.manager.save(path_to_save)

        self.show(image_frame)

    def start(self):
        self.window = Tk()
        self.window.title("PNM Manager")
        self.window.geometry("1500x1024")

        self.usage_frame = Frame(self.window, width=640)
        self.usage_frame.grid(column=0, row=0, sticky=W)

        self.image_frame = Frame(self.window)
        self.image_frame.grid(column=0, row=2)

        lbl = Label(self.usage_frame, text="enter pgm or ppm file name")
        lbl.grid(column=0, row=0)

        self.txt = Entry(self.usage_frame, width=20)
        self.txt.grid(column=1, row=0)

        btn = Button(self.usage_frame, text="read file",
                     command=lambda: self.choose_function_to_read(frame=self.image_frame))
        btn.grid(column=2, row=0)

        lbl2 = Label(self.usage_frame, text="enter new file path")
        lbl2.grid(column=0, row=1)

        self.txt2 = Entry(self.usage_frame, width=20)
        self.txt2.grid(column=1, row=1)

        btn2 = Button(self.usage_frame, text="save file",
                      command=lambda: self.choose_function_to_save(frame=self.image_frame))
        btn2.grid(column=2, row=1)

        def selected_item(event):
            current = self.color_space
            selected = combobox.get()

            if current in ["YCbCr.601", "YCbCr.709"] and selected in ["YCbCr.601", "YCbCr.709"]:
                first_standard, second_standard = current[-3:], selected[-3:]
                f = getattr(ColorSpaceConverter, f"ycbcr_{first_standard}_to_{second_standard}")
            elif current in ["YCbCr.601", "YCbCr.709"]:
                standard = current[-3:]
                f = getattr(ColorSpaceConverter, f"{current[:-4].lower()}_to_{selected.lower()}")
                self.data = f(self.data, int(standard))
            elif selected in ["YCbCr.601", "YCbCr.709"]:
                standard = selected[-3:]
                f = getattr(ColorSpaceConverter, f"{current.lower()}_to_{selected[:-4].lower()}")
                self.data = f(self.data, int(standard))
            elif current == selected:
                pass
            else:
                f = getattr(ColorSpaceConverter, f"{current.lower()}_to_{selected.lower()}")
                self.data = f(self.data)

            self.color_space = selected
            lbl_show.configure(text=f"Current color space is {self.color_space}")

            self.show(self.image_frame)

        lbl_show = Label(self.usage_frame, text=f"Current color space is {self.color_space}", width=30)
        lbl_show.grid(column=3, row=0, sticky=W)

        combobox = Combobox(self.usage_frame,
                            values=[
                                "RGB",
                                "HSL",
                                "HSV",
                                "YCbCr.601",
                                "YCbCr.709",
                                "YCoCg",
                                "CMYK"
                            ],
                            state="readonly")

        combobox.bind("<<ComboboxSelected>>", selected_item)
        combobox.grid(column=4, row=0)

        self.window.mainloop()
