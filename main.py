import pyglet
from pyglet.window import mouse
from pyglet import shapes


class HelloWorldWindow(pyglet.window.Window):

    WINDOW_SIZE = 800
    GRID_SIZE = 40
    CELL_SIZE = WINDOW_SIZE//GRID_SIZE

    def __init__(self):
        super().__init__()

        self.batch = pyglet.graphics.Batch()

        self.set_size(self.WINDOW_SIZE,self.WINDOW_SIZE)

        self.label = pyglet.text.Label("Hello, world!",
                                       x=self.width//2,
                                       y=self.height//2,
                                       anchor_x="center",
                                       anchor_y="center",
                                       font_name="Times New Roman",
                                       font_size=24)
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_HAND))
        self.rectanlgle = shapes.Rectangle(x=200,y=200,width=800,height=800,
                                      color=(250,250,250))
        self.rectanlgle.anchor_position = 200,200

        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        # self.grid_hitboxes = []
        # for r in range(self.GRID_SIZE):
        #     for c in range(self.GRID_SIZE):
        #         self.grid_hitboxes.append((r*self.CELL_SIZE+10,c*self.CELL_SIZE+10))
        # self.grid_hitboxes = tuple(self.grid_hitboxes)
        # self.grid[10][10] = 1
        
        self.running = False


    def count_neighbors(self,g, r, c):
        count = 0

        for vert in [-1,0,1]:
            for hor in [-1,0,1]:
                if vert == 0 and hor == 0:
                    continue
                nr,nc = (r+vert)%self.GRID_SIZE, (c+hor)%self.GRID_SIZE
                count += g[nr][nc]
        return count


    def update_game(self,dt):
        new_grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                neighbours = self.count_neighbors(self.grid,r,c)
                if self.grid[r][c] == 1 and (neighbours == 2 or neighbours == 3):
                    new_grid[r][c] = 1
                elif self.grid[r][c] == 0 and neighbours == 3:
                    new_grid[r][c] = 1
        self.grid = new_grid




    def on_draw(self):
        self.clear()
        self.label.draw()

        self.clear()
        cells = []

        self.rectanlgle.draw()

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.grid[r][c] == 0:
                    rect = shapes.Rectangle(
                        x=c * self.CELL_SIZE, 
                        y=r * self.CELL_SIZE, 
                        width=self.CELL_SIZE - 1, 
                        height=self.CELL_SIZE - 1, 
                        color=(46,60,114),
                        batch=self.batch
                    )
                    cells.append(rect)

                elif self.grid[r][c] == 1:
                    rect = shapes.Rectangle(
                        x=c * self.CELL_SIZE, 
                        y=r * self.CELL_SIZE, 
                        width=self.CELL_SIZE - 1, 
                        height=self.CELL_SIZE - 1, 
                        color=(50,205,50),
                        batch=self.batch
                    )
                    cells.append(rect)

        self.batch.draw()

    def on_mouse_press(self,x:int,y:int,button:int,modifiers:int):
        if button == mouse.LEFT:
            # print(x,y)
            # for r in range(self.GRID_SIZE):
            #     for c in range(self.GRID_SIZE):
            #         print(self.grid_hitboxes[r][c])

            # print(min(self.grid_hitboxes,
            #           key= lambda hb: (hb[0] - x)**2 + (hb[1] - y)**2)
            #       )

            col = int(x//self.CELL_SIZE)
            row = int(y//self.CELL_SIZE)
            print(col,row)

            if 0 <= col < self.GRID_SIZE and 0 <= row < self.GRID_SIZE:
                self.grid[row][col] = 1 - self.grid[row][col]


        if button == mouse.RIGHT:
            if not self.running:
                pyglet.clock.schedule_interval(self.update_game,0.05)
                self.running = True
            else:
                pyglet.clock.unschedule(self.update_game)
                self.running = False


if __name__ == "__main__":
    window = HelloWorldWindow()
    # print(max(window.grid_hitboxes))
    # print(window.grid_hitboxes)
    pyglet.app.run()
