from tkinter import *
import time
import math
import random

class GraphDraw:

    def __init__(self, graph=[], w=800, h=800):
        self.graph = graph
        self.width = w
        self.height = h
        self.node_radius = 14

        self.master = Tk()
        self.canvas = Canvas(self.master, width=w, height=h)
        self.canvas.pack()
        self._create_graph(self.graph)

        self.canvas.bind("<Button-1>", lambda _: self.master.quit())


    def show(self, removed=[]):
        n_nodes = len(self.graph)

        for i in range(n_nodes):
            self.canvas.itemconfig("node{}".format(i), outline="black")
            self.canvas.itemconfig("text{}".format(i), fill="black")
            self.canvas.itemconfig("conn{}".format(i), fill="black")

        n_connected = self._color_connected(removed)

        for i in removed:
            self.canvas.itemconfig("node{}".format(i), outline="#ddd", fill="white")
            self.canvas.itemconfig("text{}".format(i), fill="#ddd")
            self.canvas.itemconfig("conn{}".format(i), fill="#ddd")

        self.canvas.itemconfig("comment", text="Numero di componenti connesse: {}".format(n_connected))

        self.master.mainloop()


    def _create_graph(self, graph):
        n_nodes = len(self.graph)

        increment = 360 / n_nodes
        start_angle = 0
        for i in range(n_nodes):
            angle = start_angle + increment * i
            rads = angle * 3.14 / 180

            tx = self.width//2 + (self.width//2 - self.node_radius - 32) * math.cos(rads)
            ty = self.height//2 + (self.width//2 - self.node_radius - 32) * math.sin(rads)

            r = self.node_radius
            self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r, fill="white", tags="node{}".format(i))
            self.canvas.create_text(tx, ty, text=str(i), font=("Helvetica", 12, "bold"), tags="text{}".format(i))
            
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                if graph[i][j] == 1:
                    node1_id = self.canvas.find_withtag("node{}".format(i))[0]
                    node2_id = self.canvas.find_withtag("node{}".format(j))[0]
                    (x11, y11, x12, y12) = self.canvas.coords(node1_id)
                    (x21, y21, x22, y22) = self.canvas.coords(node2_id)
                    c1x = (x12+x11)//2
                    c1y = (y12+y11)//2
                    c2x = (x22+x21)//2
                    c2y = (y22+y21)//2
                    self.canvas.create_line(c1x, c1y, c2x, c2y, tags=("conn{}".format(i), "conn{}".format(j)))

            self.canvas.tag_raise("node{}".format(i))
            self.canvas.tag_raise("text{}".format(i))

        self.canvas.create_text(self.width//2, 8, text="", font=("Helvetica", 12), tags="comment")

    
    def _visit_connected(self, i, visited, n, color=None):
        visited[i] = 1
        if color is None:
            random.seed(2*n)
            [r, g, b] = [random.randint(127, 255), random.randint(127, 255), random.randint(127, 255)]
            color = '#%02x%02x%02x' % (r, g, b)
        self.canvas.itemconfig("node{}".format(i), fill=color)
        row = self.graph[i]
        for j in range(len(row)):
            if row[j] == 1 and visited[j] == 0:
                self._visit_connected(j, visited, n, color)


    def _color_connected(self, removed):
        visited = [0 for row in self.graph]

        # segna i nodi rimossi come visitati, cosi non vengono contati
        for i in removed:
            visited[i] = 1

        n = 0
        while sum(visited) != len(visited):
            index = visited.index(0)
            self._visit_connected(index, visited, n)
            n += 1

        return n


if __name__ == "__main__":
    import random
    n = 6
    threshold = 60
    graph = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        # Ogni riga avra' il proprio seme di casualita', dato dal tempo di sistema
        random.seed(int(time.clock() * 1000000))

        for j in range(i + 1, n):
            val = random.randint(0, 100)
            graph[i][j] = 0 if val <= threshold else 1
            graph[j][i] = graph[i][j]

    net = GraphDraw(graph)
    while 1:
        net.draw(removed=[1, 4, 5])