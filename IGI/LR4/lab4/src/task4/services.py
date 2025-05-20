import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ..task3.drawer import Drawer
from .models import Square


class SquareManager:
    def __init__(self, directory: str, drawer: Drawer):
        self._directory = directory
        self._drawer = drawer

    def draw_square(self, square: Square):
        
        fig, ax = plt.subplots()
        
        rectangle = patches.Rectangle((0-square.side/2, 0-square.side/2), square.side, square.side, color = square.color, fill = True)
        
        circle = patches.Circle((0, 0), (square.side * math.sqrt(2)/2), color='red', fill = False)
        ax.add_patch(rectangle)
        ax.add_patch(circle)
        plt.gca().set_aspect('equal', 'datalim') 
        ax.autoscale_view()
        plt.tight_layout()
        plt.title('Square with circle')
        plt.show()

        plt.savefig(f"{self._directory}square_with_circle.png")
        