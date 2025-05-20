import matplotlib.pyplot as plt


class Drawer(object):

    def __init__(self):

        self._colors = ('b-', 'r-', 'g-', 'c-', 'm-', 'y-', 'k-')

    def plot_table(self,
                   graphics: tuple[tuple[tuple[float, ...], tuple[float, ...]], ...],
                   coord_names: tuple[str, str],
                   graphic_names: tuple[str, ...],
                   title: str,
                   filename: str):

        plt.figure(figsize=(10, 6))

        for i, graphic in enumerate(graphics):
            plt.plot(*graphic, self._colors[i], label=graphic_names[i])

        self._set_plot_settings(*coord_names, title=title)

        plt.savefig(filename)
        plt.show()

    def plot_by_coords(self,
                       x: tuple[float, ...],
                       y: tuple[float, ...],
                       title: str,
                       filename: str,
                       color: str = 'b-'):


        plt.savefig(filename)
        plt.scatter(x[:-1], y[:-1], color='black')

        self._set_plot_settings('x', 'y', title, legend=False)
        plt.axis("equal")
        
        plt.show()
        
        

    @staticmethod
    def _set_plot_settings(x: str, y: str, title: str, legend: bool = True):

        plt.grid(True)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        if legend:
            plt.legend()
