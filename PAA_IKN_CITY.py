from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import ttk
import random

# Konstanta ukuran peta
MAP_SIZE = 150
CELL_SIZE = 32  # Disesuaikan dengan ukuran gambar per cell

# Konstanta untuk berbagai jenis jalan
EMPTY = 0
ROAD = 'road'
CROSSROAD = 'crossroad'
T_JUNCTION = 't_junction'
TURN = 'turn'

# Batas jumlah jenis jalan
CROSSROAD_LIMIT = 5
T_JUNCTION_LIMIT = 10
TURN_LIMIT = 15

# Jarak minimal antara jalan
MIN_DISTANCE = 5

# Konstanta ukuran bangunan
BIG_BUILDING = 'big_building'
MEDIUM_BUILDING = 'orange'
SMALL_BUILDING = 'abu'
HOUSE = 'house'
TREE = 'tree'
BUSH = 'bush'

BUILDING_SIZES = {
    BIG_BUILDING: (5, 10),
    MEDIUM_BUILDING: (5, 3),
    SMALL_BUILDING: (2, 2),
    HOUSE: (2, 1),
    TREE: (2, 1),
    BUSH: (1, 1)
}

BUILDING_IMAGES = {
    BIG_BUILDING: 'big_building.png',
    MEDIUM_BUILDING: 'orange.png',
    SMALL_BUILDING: 'merahmerah.jpg',
    HOUSE: 'house.png',
    TREE: 'tree.png',
    BUSH: 'bush.png'
}

BUILDING_MINIMUMS = {
    BIG_BUILDING: 40,
    MEDIUM_BUILDING: 50,
    SMALL_BUILDING: 80,
    HOUSE: 200,
    TREE: 500,
    BUSH: 500
}

class MapGenerator:
    def __init__(self, size):
        self.size = size
        self.map = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        # Kosongkan peta
        self.map = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        crossroad_count = 0
        t_junction_count = 0
        turn_count = 0

        while crossroad_count < CROSSROAD_LIMIT or t_junction_count < T_JUNCTION_LIMIT or turn_count < TURN_LIMIT:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.map[x][y] == EMPTY and self.is_location_valid(x, y):
                if crossroad_count < CROSSROAD_LIMIT:
                    self.map[x][y] = CROSSROAD
                    self.extend_road(x, y, 'up')
                    self.extend_road(x, y, 'down')
                    self.extend_road(x, y, 'left')
                    self.extend_road(x, y, 'right')
                    crossroad_count += 1
                elif t_junction_count < T_JUNCTION_LIMIT:
                    direction = random.choice(['up', 'down', 'left', 'right'])
                    if direction == 'up':
                        self.map[x][y] = 'tjunction_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down':
                        self.map[x][y] = 'tjunction_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'right')
                    elif direction == 'left':
                        self.map[x][y] = 'tjunction_left'
                        self.extend_road(x, y, 'left')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    elif direction == 'right':
                        self.map[x][y] = 'tjunction_right'
                        self.extend_road(x, y, 'right')
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'down')
                    t_junction_count += 1
                elif turn_count < TURN_LIMIT:
                    direction = random.choice(['up-right', 'up-left', 'down-right', 'down-left'])
                    if direction == 'up-right':
                        self.map[x][y] = 'turn_right_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'right')
                    elif direction == 'up-left':
                        self.map[x][y] = 'turn_left_up'
                        self.extend_road(x, y, 'up')
                        self.extend_road(x, y, 'left')
                    elif direction == 'down-right':
                        self.map[x][y] = 'turn_right_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'right')
                    elif direction == 'down-left':
                        self.map[x][y] = 'turn_left_down'
                        self.extend_road(x, y, 'down')
                        self.extend_road(x, y, 'left')
                    turn_count += 1

        self.place_buildings()
        self.place_bushes()

    def is_location_valid(self, x, y, width=1, height=1):
        for i in range(max(0, x - MIN_DISTANCE), min(self.size, x + width + MIN_DISTANCE)):
            for j in range(max(0, y - MIN_DISTANCE), min(self.size, y + height + MIN_DISTANCE)):
                if self.map[i][j] != EMPTY:
                    return False
        return True

    def extend_road(self, x, y, direction):
        if direction == 'up':
            for i in range(x-1, -1, -1):
                if self.map[i][y] != EMPTY:
                    if self.map[i][y] == 'vertical_road':
                        self.map[i][y] = CROSSROAD
                    elif self.map[i][y] == 'horizontal_road':
                        self.map[i][y] = 'tjunction_down'
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'down':
            for i in range(x+1, self.size):
                if self.map[i][y] != EMPTY:
                    if self.map[i][y] == 'vertical_road':
                        self.map[i][y] = CROSSROAD
                    elif self.map[i][y] == 'horizontal_road':
                        self.map[i][y] = 'tjunction_up'
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'left':
            for j in range(y-1, -1, -1):
                if self.map[x][j] != EMPTY:
                    if self.map[x][j] == 'horizontal_road':
                        self.map[x][j] = CROSSROAD
                    elif self.map[x][j] == 'vertical_road':
                        self.map[x][j] = 'tjunction_right'
                    break
                self.map[x][j] = 'horizontal_road'
        elif direction == 'right':
            for j in range(y+1, self.size):
                if self.map[x][j] != EMPTY:
                    if self.map[x][j] == 'horizontal_road':
                        self.map[x][j] = CROSSROAD
                    elif self.map[x][j] == 'vertical_road':
                        self.map[x][j] = 'tjunction_left'
                    break
                self.map[x][j] = 'horizontal_road'

    def place_buildings(self):
        for building, minimum in BUILDING_MINIMUMS.items():
            if building == BUSH:
                continue
            count = 0
            while count < minimum:
                x = random.randint(0, self.size - BUILDING_SIZES[building][0])
                y = random.randint(0, self.size - BUILDING_SIZES[building][1])
                if self.is_location_valid_for_building(x, y, BUILDING_SIZES[building][0], BUILDING_SIZES[building][1]):
                    for i in range(x, x + BUILDING_SIZES[building][0]):
                        for j in range(y, y + BUILDING_SIZES[building][1]):
                            self.map[i][j] = building
                    count += 1

    def place_bushes(self):
        count = 0
        while count < BUILDING_MINIMUMS[BUSH]:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.map[x][y] == EMPTY:
                self.map[x][y] = BUSH
                count += 1

    def is_location_valid_for_building(self, x, y, width, height):
        # Cek apakah ada cell di area yang diusulkan adalah jalan atau bangunan lain
        for i in range(x, x + width):
            for j in range(y, y + height):
                if self.map[i][j] != EMPTY:
                    return False
        # Periksa jarak minimum ke jalan
        road_found = False
        for i in range(max(0, x - 1), min(self.size, x + width + 1)):
            for j in range(max(0, y - 1), min(self.size, y + height + 1)):
                if self.map[i][j] in ['vertical_road', 'horizontal_road', CROSSROAD, 'tjunction_up', 'tjunction_down', 'tjunction_left', 'tjunction_right', 'turn_right_up', 'turn_left_up', 'turn_right_down', 'turn_left_down']:
                    road_found = True
                # Pastikan jarak minimal 2 cell dari bangunan lain
                if i in range(x, x + width) and j in range(y, y + height):
                    continue
                if self.map[i][j] in BUILDING_SIZES:
                    return False
        return road_found

    def get_map(self):
        return self.map

class MapDisplay(tk.Frame):
    def __init__(self, parent, map_data):
        super().__init__(parent)
        self.parent = parent
        self.map_data = map_data

        # Frame untuk kanvas peta dan tombol
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kanvas untuk menampilkan peta
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tambahkan scrollbar
        self.h_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        # Frame untuk tombol
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.N)

        self.redesign_button = ttk.Button(self.button_frame, text="Redesign", command=self.redesign_map)
        self.redesign_button.pack(pady=10)

        # Tambahkan label judul
        self.title_label = ttk.Label(self.button_frame, text="Random Map Generator", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Tambahkan instruksi
        self.instruction_label = ttk.Label(self.button_frame, text="Peta akan digambar ulang", font=("Helvetica", 10))
        self.instruction_label.pack(pady=10)

        # Bind keys and mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind_all("<KeyPress>", self.on_key_press)

        # Variables for dragging
        self.start_x = None
        self.start_y = None

        # Draw initial map
        self.draw_map()

    def draw_map(self):
        # Buat gambar baru
        img = Image.new("RGB", (MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE), "white")
        draw = ImageDraw.Draw(img)

        # Load images
        images = {
            'vertical_road': Image.open("Assets/vertical_road.png"),
            'horizontal_road': Image.open("Assets/horizontal_road.png"),
            'crossroad': Image.open("Assets/crossroad.png"),
            'tjunction_up': Image.open("Assets/tjunction_up.png"),
            'tjunction_down': Image.open("Assets/tjunction_down.png"),
            'tjunction_left': Image.open("Assets/tjunction_left.png"),
            'tjunction_right': Image.open("Assets/tjunction_right.png"),
            'turn_left_down': Image.open("Assets/turn_left_down.png"),
            'turn_left_up': Image.open("Assets/turn_left_up.png"),
            'turn_right_up': Image.open("Assets/turn_right_up.png"),
            'turn_right_down': Image.open("Assets/turn_right_down.png"),
            BIG_BUILDING: Image.open(f"Assets/{BUILDING_IMAGES[BIG_BUILDING]}"),
            MEDIUM_BUILDING: Image.open(f"Assets/{BUILDING_IMAGES[MEDIUM_BUILDING]}"),
            SMALL_BUILDING: Image.open(f"Assets/{BUILDING_IMAGES[SMALL_BUILDING]}"),
            HOUSE: Image.open(f"Assets/{BUILDING_IMAGES[HOUSE]}"),
            TREE: Image.open(f"Assets/{BUILDING_IMAGES[TREE]}"),
            BUSH: Image.open(f"Assets/{BUILDING_IMAGES[BUSH]}"),
            'grass': Image.open("Assets/grass.png")  # Tambahkan gambar rumput
        }

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell_type = self.map_data[i][j]
                if cell_type in images:
                    if cell_type in BUILDING_SIZES:
                        building_size = BUILDING_SIZES[cell_type]
                        if self.is_top_left_of_building(i, j, building_size):
                            img.paste(images[cell_type], (j * CELL_SIZE, i * CELL_SIZE))
                    else:
                        img.paste(images[cell_type], (j * CELL_SIZE, i * CELL_SIZE))
                else:
                    img.paste(images['grass'], (j * CELL_SIZE, i * CELL_SIZE))

        # Tampilkan gambar di Tkinter
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def is_top_left_of_building(self, i, j, building_size):
        if i + building_size[0] <= MAP_SIZE and j + building_size[1] <= MAP_SIZE:
            for x in range(building_size[0]):
                for y in range(building_size[1]):
                    if self.map_data[i + x][j + y] != self.map_data[i][j]:
                        return False
            return True
        return False

    def redesign_map(self):
        # Generate new map data
        map_generator = MapGenerator(MAP_SIZE)
        self.map_data = map_generator.get_map()
        # Redraw map
        self.draw_map()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.xview_scroll(-dx, 'units')
        self.canvas.yview_scroll(-dy, 'units')
        self.start_x = event.x
        self.start_y = event.y

    def on_key_press(self, event):
        if event.keysym == 'Left':
            self.canvas.xview_scroll(-1, 'units')
        elif event.keysym == 'Right':
            self.canvas.xview_scroll(1, 'units')
        elif event.keysym == 'Up':
            self.canvas.yview_scroll(-1, 'units')
        elif event.keysym == 'Down':
            self.canvas.yview_scroll(1, 'units')

def main():
    root = tk.Tk()
    root.title("Random Map Generator")

    # Tambahkan style untuk memperindah UI
    style = ttk.Style(root)
    style.theme_use('clam')  # Pilihan tema yang lebih modern

    map_generator = MapGenerator(MAP_SIZE)
    map_data = map_generator.get_map()
    map_display = MapDisplay(root, map_data)
    map_display.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
