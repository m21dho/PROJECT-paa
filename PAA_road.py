from PIL import Image, ImageTk
import tkinter as tk
import random

# Konstanta ukuran peta
MAP_SIZE = 150
CELL_SIZE = 32 

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


class MapGenerator:
    def __init__(self, size):
        self.size = size
        self.map = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        # Clear the map
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
                        self.map[i][y] = 'crossroad'
                    elif self.map[i][y] == 'horizontal_road':
                        self.map[i][y] = 'tjunction_down'
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'down':
            for i in range(x+1, self.size):
                if self.map[i][y] != EMPTY:
                    if self.map[i][y] == 'vertical_road':
                        self.map[i][y] = 'crossroad'
                    elif self.map[i][y] == 'horizontal_road':
                        self.map[i][y] = 'tjunction_up'
                    break
                self.map[i][y] = 'vertical_road'
        elif direction == 'left':
            for j in range(y-1, -1, -1):
                if self.map[x][j] != EMPTY:
                    if self.map[x][j] == 'horizontal_road':
                        self.map[x][j] = 'crossroad'
                    elif self.map[x][j] == 'vertical_road':
                        self.map[x][j] = 'tjunction_right'
                    break
                self.map[x][j] = 'horizontal_road'
        elif direction == 'right':
            for j in range(y+1, self.size):
                if self.map[x][j] != EMPTY:
                    if self.map[x][j] == 'horizontal_road':
                        self.map[x][j] = 'crossroad'
                    elif self.map[x][j] == 'vertical_road':
                        self.map[x][j] = 'tjunction_left'
                    break
                self.map[x][j] = 'horizontal_road'

    def get_map(self):
        return self.map

class MapDisplay(tk.Frame):
    def __init__(self, parent, map_data):
        super().__init__(parent)
        self.parent = parent
        self.map_data = map_data
        self.scale = 1.0

        # Load images
        self.images = {
            'vertical_road': ImageTk.PhotoImage(Image.open("Assets/vertical_road.png")),
            'horizontal_road': ImageTk.PhotoImage(Image.open("Assets/horizontal_road.png")),
            'crossroad': ImageTk.PhotoImage(Image.open("Assets/crossroad.png")),
            'tjunction_up': ImageTk.PhotoImage(Image.open("Assets/tjunction_up.png")),
            'tjunction_down': ImageTk.PhotoImage(Image.open("Assets/tjunction_down.png")),
            'tjunction_left': ImageTk.PhotoImage(Image.open("Assets/tjunction_left.png")),
            'tjunction_right': ImageTk.PhotoImage(Image.open("Assets/tjunction_right.png")),
            'turn_left_down': ImageTk.PhotoImage(Image.open("Assets/turn_left_down.png")),
            'turn_left_up': ImageTk.PhotoImage(Image.open("Assets/turn_left_up.png")),
            'turn_right_up': ImageTk.PhotoImage(Image.open("Assets/turn_right_up.png")),
            'turn_right_down': ImageTk.PhotoImage(Image.open("Assets/turn_right_down.png")),
            'grass': ImageTk.PhotoImage(Image.open("Assets/grass.png")) 
        }

        # Frame untuk kanvas peta dan tombol
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kanvas untuk menampilkan peta dengan scrollbars
        self.canvas = tk.Canvas(self.main_frame, bg="white", scrollregion=(0, 0, MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE))
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.hbar = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky=tk.EW)
        self.vbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.draw_map()

        # Frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=2, padx=10, pady=10, sticky=tk.N)

        self.redesign_button = tk.Button(self.button_frame, text="Redesign", command=self.redesign_map)
        self.redesign_button.pack()

        # Bind arrow keys for panning
        self.canvas.bind_all("<Up>", self.pan_up)
        self.canvas.bind_all("<Down>", self.pan_down)
        self.canvas.bind_all("<Left>", self.pan_left)
        self.canvas.bind_all("<Right>", self.pan_right)

    def draw_map(self):
        self.canvas.delete("all")
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell_type = self.map_data[i][j]
                if cell_type in self.images:
                        self.canvas.create_image(j * CELL_SIZE * self.scale, i * CELL_SIZE * self.scale, anchor=tk.NW, image=self.images[cell_type])
                else:
                    self.canvas.create_image(j * CELL_SIZE * self.scale, i * CELL_SIZE * self.scale, anchor=tk.NW, image=self.images['grass'])

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


    def pan_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def pan_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def pan_left(self, event):
        self.canvas.xview_scroll(-1, "units")

    def pan_right(self, event):
        self.canvas.xview_scroll(1, "units")

def main():
    root = tk.Tk()
    root.title("Random Map Generator")

    map_generator = MapGenerator(MAP_SIZE)
    map_data = map_generator.get_map()
    map_display = MapDisplay(root, map_data)
    map_display.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
