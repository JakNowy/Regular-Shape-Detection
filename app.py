from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from app_lidar import LidarImage

class Application():
    def __init__(self):
        ### Window Creation ###

        # Parameters
        self.color1 = 'ghostwhite'  # button hover
        self.color2 = 'ivory3'  # button bg
        self.color3 = "goldenrod2"  # bg

        self.button_width = 40
        self.entry_width = 8

        self.window = Tk()
        self.window.minsize(width='400', height='500')
        self.window.winfo_toplevel().title('GeoImage 2018')
        self.window.config(bg=self.color1)

        # Softcapping the grid
        self.rn = 10  # reference row number
        self.cn = 1  # reference column number

        # Drawing parameters
        self.color = (50, 250, 100)  # BGR; color of drawn circles
        self.thickness = 2  # thickness of found circles when drawn

        self.LIDAR = False

    def create_grid(self, frame, rows, cols):
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        for i in range(rows):
            frame.rowconfigure(i, weight=1)

    def generate(self, event=None):
        mat_shape = self.mat_shape.get().split(',')
        self.mat_shape_get = []
        self.mat_shape_get.append(int(mat_shape[0]))
        self.mat_shape_get.append(int(mat_shape[1]))

        self.number_of_points_get = int(self.number_of_points.get())
        self.z_max_get = int(self.z_max.get())
        z_range = self.z_range.get().split(',')
        self.z_range_get = []
        self.z_range_get.append(int(z_range[0]))
        self.z_range_get.append(int(z_range[1]))

        self.LIDAR = True

        l = open(self.file).read()
        self.points = []
        l = l.split(',')
        for i in l:
            i = i.split(',')
            j = (i[0],i[1],i[2])
            self.points.append(j)
        print(self.points)

        self.img = LidarImage(self.mat_shape_get, self.points, self.number_of_points_get, self.z_max_get)
        self.img = self.img.LIDAR_to_raster(self.z_range_get)

    def read_file(self, event=None):
        self.file = filedialog.askopenfilename()

    def read_lidar(self, event=None):
        self.lidar_window = Tk()
        self.lidar_window.minsize(width='300', height='250')
        self.lidar_window.winfo_toplevel().title('Lidar Data')
        self.lidar_window.config(bg=self.color3)

        self.create_grid(self.lidar_window, 10,10)

        # Labels
        lidar_data = Button(self.lidar_window, text='Read from file', cursor='hand2')
        lidar_data.bind('<Button-1>', self.read_file)

        self.mat_shape = Entry(self.lidar_window, width = self.entry_width)
        mat_shape_lab = Label(self.lidar_window,text='Matrix shape [ (X,Y) ]:', bg=self.color3)

        random_params = Label(self.lidar_window, text='Random points parameters:', bg=self.color3)

        self.number_of_points = Entry(self.lidar_window, width=self.entry_width)
        number_of_points_lab = Label(self.lidar_window, text = 'Number of points to generate:', bg=self.color3)

        self.z_max= Entry(self.lidar_window, width=self.entry_width)
        z_max_lab = Label(self.lidar_window, text = 'z-max:', bg=self.color3)

        self.z_range = Entry(self.lidar_window, width=self.entry_width)
        z_range_lab = Label(self.lidar_window, text = 'z-range:', bg=self.color3)

        random = Button(self.lidar_window, text='Generate points', cursor='hand2')
        random.bind('<Button-1>', self.generate)

        OK = Button(self.lidar_window, text='OK', cursor='hand2', command=self.lidar_window.destroy)

        # Grid
        mat_shape_lab.grid(in_=self.lidar_window, row=1, column=1)
        self.mat_shape.grid(in_=self.lidar_window, row=1, column=2, sticky=E)

        lidar_data.grid(in_=self.lidar_window, row=2, column=1)

        random_params.grid(in_=self.lidar_window, row= 3, column=1)

        number_of_points_lab.grid(in_=self.lidar_window, row=4, column=1)
        self.number_of_points.grid(in_=self.lidar_window, row=4, column=2, sticky=E)

        z_max_lab.grid(in_=self.lidar_window, row=5, column=1)
        self.z_max.grid(in_=self.lidar_window, row=5, column=2, sticky=E)

        z_range_lab.grid(in_=self.lidar_window, row=6, column=1)
        self.z_range.grid(in_=self.lidar_window, row=6, column=2, sticky=E)

        random.grid(in_=self.lidar_window, row = 8, column=1)
        OK.grid(in_=self.lidar_window, row=8, column=2)

    def menu(self, event=None):
        try:
            self.lines_frame.destroy()
            self.circles_frame.destroy()
        except AttributeError:
            pass

        # Create menu frame
        self.menu_frame = Frame(self.window)
        self.menu_frame.config(bg=self.color3)
        self.menu_frame.pack(fill='both', expand=True)

        self.create_grid(self.menu_frame, 20, 10)

        # Widget creation
        lab_menu_frame = Label(self.menu_frame, text='Welcome to GeoImage!', font=1, bg=self.color3)

        but_lines = Menubutton(self.menu_frame, text='Line Detection', width=self.button_width, bg=self.color2,
                               activebackground=self.color1, cursor='hand2')
        but_lines.bind('<Button-1>', self.lines)

        but_circles = Menubutton(self.menu_frame, text='Circle Detection', width=self.button_width, bg=self.color2,
                                 activebackground=self.color1, cursor='hand2')
        but_circles.bind('<Button-1>', self.circles)

        but_exit = Menubutton(self.menu_frame, text='Exit', width=self.button_width, bg=self.color2,
                              activebackground=self.color1, cursor='hand2')
        but_exit.bind('<Button-1>', self.exit)


        # Widget positioning
        lab_menu_frame.grid(in_=self.menu_frame, row=self.rn - 5, column=self.cn, columnspan=8, rowspan=2)
        but_lines.grid(in_=self.menu_frame, row=self.rn + 1, column=self.cn, columnspan=8)
        but_circles.grid(in_=self.menu_frame, row=self.rn + 2, column=self.cn, columnspan=8)
        but_exit.grid(in_=self.menu_frame, row=self.rn + 3, column=self.cn, columnspan=8)

        self.window.mainloop()

    def lines(self, event=None):

        # Create lines frame
        self.menu_frame.destroy()

        self.lines_frame = Frame(self.window)
        self.lines_frame.config(bg=self.color3)
        self.lines_frame.pack(fill='both', expand=True)

        self.create_grid(self.lines_frame, 20, 10)

        # Widget creation
        lines_lab = Label(self.lines_frame, text='Line detection', bg=self.color3)
        lines_lab.config(font=60)

        file_lab = Label(self.lines_frame, text='Image: ', bg=self.color3)

        file_entry = Button(self.lines_frame, text='Read an image', cursor='hand2')
        file_entry.bind('<Button-1>', self.read_file)

        lidar_entry = Button(self.lines_frame, text='Read lidar', cursor='hand2')
        lidar_entry.bind('<Button-1>', self.read_lidar)

        self.isLIDAR = IntVar()
        # lidar = Checkbutton(self.lines_frame, text='LIDAR data', variable=self.isLIDAR, bg=self.color3)

        self.grayscale = IntVar()
        grayscale = Checkbutton(self.lines_frame, text='Convert to grayscale', variable=self.grayscale, bg=self.color3)

        edge_label = Label(self.lines_frame, text='Edge detection parameters: ', bg=self.color3)

        self.t1 = Entry(self.lines_frame, width = self.entry_width)
        self.t2 = Entry(self.lines_frame, width = self.entry_width)

        t1_lab = Label(self.lines_frame, text='Threshold1:', bg=self.color3)
        t2_lab = Label(self.lines_frame, text='Threshold2:', bg=self.color3)

        detection_lab = Label(self.lines_frame, text='Line detection parameters:', bg=self.color3)

        self.rho = Entry(self.lines_frame, width = self.entry_width)
        rho_lab = Label(self.lines_frame, text='Rho:', bg=self.color3)

        self.theta = Entry(self.lines_frame, width = self.entry_width)
        theta_lab = Label(self.lines_frame, text='Theta:', bg=self.color3)

        self.threshold = Entry(self.lines_frame, width = self.entry_width)
        threshold_lab = Label(self.lines_frame, text='Threshold:', bg=self.color3)

        self.min_length= Entry(self.lines_frame, width = self.entry_width)
        min_length_lab = Label(self.lines_frame, text='Min Line Length:', bg=self.color3)

        self.max_gap = Entry(self.lines_frame, width = self.entry_width)
        max_gap_lab = Label(self.lines_frame, text='Max Line Gap: ', bg=self.color3)

        return_btn = Button(self.lines_frame, text='Back')
        return_btn.bind('<Button-1>', self.menu)

        calc_lines_btn = Button(self.lines_frame, text='Calculate')
        calc_lines_btn.bind('<Button-1>', self.calc_lines)

        # Widget positioning
        lines_lab.grid(in_=self.lines_frame, row=self.rn-9, column=self.cn+2)

        file_lab.grid(in_=self.lines_frame, row=self.rn-8, column=self.cn+1, sticky=E)
        file_entry.grid(in_=self.lines_frame, row = self.rn-8, column = self.cn+2)
        lidar_entry.grid(in_=self.lines_frame, row = self.rn-8, column = self.cn+3)
        # lidar.grid(in_=self.lines_frame, row=self.rn-8, column=self.cn+3, sticky=W)
        grayscale.grid(in_=self.lines_frame, row=self.rn-7, column=self.cn+1, sticky=W)
        edge_label.grid(in_=self.lines_frame, row=self.rn-6, column=self.cn+1, sticky=W)
        self.t1.grid(in_=self.lines_frame, row=self.rn-5, column=self.cn+2, sticky=W)
        self.t2.grid(in_=self.lines_frame, row=self.rn-4, column=self.cn+2, sticky=W)
        t1_lab.grid(in_=self.lines_frame, row=self.rn-5, column=self.cn+1, sticky=E)
        t2_lab.grid(in_=self.lines_frame, row=self.rn-4, column=self.cn+1, sticky=E)

        detection_lab.grid(in_=self.lines_frame, row=self.rn-3, column=self.cn+1)

        self.rho.grid(in_=self.lines_frame, row=self.rn-2, column=self.cn+2, sticky=W)
        rho_lab.grid(in_=self.lines_frame, row=self.rn-2, column=self.cn+1, sticky=E)

        self.theta.grid(in_=self.lines_frame, row=self.rn-1, column=self.cn+2, sticky=W)
        theta_lab.grid(in_=self.lines_frame, row=self.rn-1, column=self.cn+1, sticky=E)

        self.threshold.grid(in_=self.lines_frame, row=self.rn, column=self.cn+2, sticky=W)
        threshold_lab.grid(in_=self.lines_frame, row=self.rn, column=self.cn+1, sticky=E)

        self.min_length.grid(in_=self.lines_frame, row=self.rn+1, column=self.cn+2, sticky=W)
        min_length_lab.grid(in_=self.lines_frame, row=self.rn+1, column=self.cn+1, sticky=E)

        self.max_gap.grid(in_=self.lines_frame, row=self.rn+2, column=self.cn+2, sticky=W)
        max_gap_lab.grid(in_=self.lines_frame, row=self.rn+2, column=self.cn+1, sticky=E)

        return_btn.grid(in_=self.lines_frame, row=self.rn+6, column=self.cn+1)
        calc_lines_btn.grid(in_=self.lines_frame, row=self.rn+6, column=self.cn+3)

    def circles(self, event=None):

        # Create circles frame
        self.menu_frame.destroy()

        self.circles_frame = Frame(self.window)
        self.circles_frame.config(bg=self.color3)
        self.circles_frame.pack(fill='both', expand=True)

        self.create_grid(self.circles_frame, 20, 10)

        # Widget creation
        circles_lab = Label(self.circles_frame, text='Circle detection', bg=self.color3)
        circles_lab.config(font=60)

        file_lab = Label(self.circles_frame, text='Image: ', bg=self.color3)

        file_entry = Button(self.circles_frame, text='Read an image', cursor='hand2')
        file_entry.bind('<Button-1>', self.read_file)

        lidar_entry = Button(self.circles_frame, text='Read lidar', cursor='hand2')
        lidar_entry.bind('<Button-1>', self.read_lidar)

        self.isLIDAR = IntVar()
        lidar = Checkbutton(self.circles_frame, text='LIDAR data', variable=self.isLIDAR, bg=self.color3)

        self.grayscale = IntVar()
        grayscale = Checkbutton(self.circles_frame, text='Convert to grayscale', variable=self.grayscale, bg=self.color3)

        edge_label = Label(self.circles_frame, text='Edge detection parameters:', bg=self.color3)

        self.t1 = Entry(self.circles_frame, width = self.entry_width)
        # t2 = Entry(self.circles_frame, width = self.entry_width)

        t1_lab = Label(self.circles_frame, text='Threshold1:', bg=self.color3)
        # t2_lab = Label(self.circles_frame, text='Threshold2:', bg=self.color3)

        detection_lab = Label(self.circles_frame, text='Circle detection parameters:', bg=self.color3)

        self.res_ratio = Entry(self.circles_frame, width = self.entry_width)
        res_ratio_lab = Label(self.circles_frame, text='Res. ratio:', bg=self.color3)

        self.circ_dist = Entry(self.circles_frame, width = self.entry_width)
        circ_dist_lab = Label(self.circles_frame, text='Minimum circle distance:', bg=self.color3)

        self.points_per_circle = Entry(self.circles_frame, width = self.entry_width)
        points_per_circle_lab = Label(self.circles_frame, text='Min points per circle:', bg=self.color3)

        self.min_radius = Entry(self.circles_frame, width = self.entry_width)
        min_radius_lab = Label(self.circles_frame, text='Min Radius:', bg=self.color3)

        self.max_radius = Entry(self.circles_frame, width = self.entry_width)
        max_radius_lab = Label(self.circles_frame, text='Max Radius: ', bg=self.color3)

        return_btn = Button(self.circles_frame, text='Back')
        return_btn.bind('<Button-1>', self.menu)

        calc_circles_btn = Button(self.circles_frame, text='Calculate')
        calc_circles_btn.bind('<Button-1>', self.calc_circles)

        # Widget positioning
        circles_lab.grid(in_=self.circles_frame, row=self.rn-9, column=self.cn+2)

        file_lab.grid(in_=self.circles_frame, row=self.rn-8, column=self.cn+1, sticky=E)
        file_entry.grid(in_=self.circles_frame, row = self.rn-8, column = self.cn+2)
        lidar_entry.grid(in_=self.circles_frame, row = self.rn-8, column = self.cn+3)
        # lidar.grid(in_=self.circles_frame, row=self.rn-8, column=self.cn+3, sticky=W)
        grayscale.grid(in_=self.circles_frame, row=self.rn-7, column=self.cn+1, sticky=W)
        edge_label.grid(in_=self.circles_frame, row=self.rn-6, column=self.cn+1, sticky=W)
        self.t1.grid(in_=self.circles_frame, row=self.rn-5, column=self.cn+2, sticky=W)
        t1_lab.grid(in_=self.circles_frame, row=self.rn-5, column=self.cn+1, sticky=E)
        # t2.grid(in_=self.circles_frame, row=self.rn-4, column=self.cn+2, sticky=W)
        # t2_lab.grid(in_=self.circles_frame, row=self.rn-4, column=self.cn+1, sticky=E)

        detection_lab.grid(in_=self.circles_frame, row=self.rn-3, column=self.cn+1)

        self.res_ratio.grid(in_=self.circles_frame, row=self.rn-2, column=self.cn+2, sticky=W)
        res_ratio_lab.grid(in_=self.circles_frame, row=self.rn-2, column=self.cn+1, sticky=E)

        self.circ_dist.grid(in_=self.circles_frame, row=self.rn-1, column=self.cn+2, sticky=W)
        circ_dist_lab.grid(in_=self.circles_frame, row=self.rn-1, column=self.cn+1, sticky=E)

        self.points_per_circle.grid(in_=self.circles_frame, row=self.rn, column=self.cn+2, sticky=W)
        points_per_circle_lab.grid(in_=self.circles_frame, row=self.rn, column=self.cn+1, sticky=E)

        self.min_radius.grid(in_=self.circles_frame, row=self.rn+1, column=self.cn+2, sticky=W)
        min_radius_lab.grid(in_=self.circles_frame, row=self.rn+1, column=self.cn+1, sticky=E)

        self.max_radius.grid(in_=self.circles_frame, row=self.rn+2, column=self.cn+2, sticky=W)
        max_radius_lab.grid(in_=self.circles_frame, row=self.rn+2, column=self.cn+1, sticky=E)

        return_btn.grid(in_=self.circles_frame, row=self.rn+6, column=self.cn+1)
        calc_circles_btn.grid(in_=self.circles_frame, row=self.rn+6, column=self.cn+3)

    def exit(self, event=None):
        self.window.destroy()

    def calc_circles(self, event=None):
        self.threshold_get = int(self.t1.get())
        self.res_ratio_get = float(self.res_ratio.get())
        self.circ_dist_get = int(self.circ_dist.get())
        self.points_per_circle_get = int(self.points_per_circle.get())
        self.min_radius_get = int(self.min_radius.get())
        self.max_radius_get = int(self.max_radius.get())

        # Read Image
        if not self.LIDAR:
            self.img = cv2.imread(self.file)
        self.img_color = self.img
        # Grayscale Convertion
        if self.grayscale:
            self.img = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)

        # Gaussian Blur
        self.img = cv2.GaussianBlur(self.img, (5, 5), 1.5)

        circles = cv2.HoughCircles(self.img, cv2.HOUGH_GRADIENT, dp=self.res_ratio_get, minDist=self.circ_dist_get,
                               param2=self.points_per_circle_get, minRadius=self.min_radius_get, maxRadius=self.max_radius_get)
        circles = np.uint16(np.around(circles))
        circles_found = 0
        coordinates = ''

        for circle in circles[0]:
            cv2.circle(self.img_color, (circle[0], circle[1]), circle[2], self.color, self.thickness)
            circles_found += 1
            coordinates += f'{circles_found}. A = {circle[0]}, B = {circle[1]}, R = {circle[2]}\n'

        # fname = self.file.split('.')
        # print(fname)
        # cv2.imwrite(f'{fname[0]} transformed.{fname[-1]}', img)
        # with open(f'{fname[0]} transformed data.txt', 'w') as datafile:
        #     message = f'{circles_found} circles has been found in total: \n\n{coordinates}\nLegend:\n' \
        #               f'(A,B - coordinates of the center, ' \
        #               f'R - range)\n\n\n'
        #     data = f'Transformation parameters:\n\n' \
        #            f'Original file name : {file_name}\n' \
        #            f'Dp : {dp}\n' \
        #            f'Distance beetween circles: : {circle_distance}\n' \
        #            f'Points required to treat as circle : {min_points_per_circle}\n' \
        #            f'Minimal circle radius : {min_radius}\n' \
        #            f'Maximal circle radius : {max_radius}\n'
        #     datafile.write(f'{message}{data}')

        path = self.file.split('/')[-1]
        cv2.imshow('img',self.img_color)
        cv2.imwrite(path,self.img_color)


    def calc_lines(self, event=None):
        self.rho_get = int(self.rho.get())
        self.theta_get = float(self.theta.get())
        self.threshold_get = int(self.threshold.get())
        self.t1_get = int(self.t1.get())
        self.t2_get = int(self.t2.get())
        self.min_length_get = int(self.min_length.get())
        self.max_gap_get = int(self.max_gap.get())

        self.grayscale_get = self.grayscale.get()
        self.isLIDAR_get = self.isLIDAR.get()

        # Read Image
        if not self.LIDAR:
            self.img = cv2.imread(self.file)
        self.img_color = self.img

        # Grayscale Convertion
        if self.grayscale:
            img = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)

        # Gaussian Blur
        self.img = cv2.GaussianBlur(self.img, (5, 5), 1.5)

        # Canny Edge Detection
        self.img = cv2.Canny(self.img, self.t1_get, self.t2_get)


        # Hough Lines
        lines = cv2.HoughLinesP(self.img, self.rho_get, self.theta_get, self.threshold_get,
                              minLineLength=self.min_length_get, maxLineGap=self.max_gap_get)

        # cv2.line(self.img_color, (50, 50), (100, 100), (100, 100, 100), 5)

        for line in lines:
            cv2.line(self.img_color, (line[0][0], line[0][1]),(line[0][2], line[0][3]), self.color, thickness=self.thickness)


        path = self.file.split('/')[-1]
        cv2.imshow('img',self.img_color)
        cv2.imwrite(path,self.img_color)
app = Application()
app.menu()