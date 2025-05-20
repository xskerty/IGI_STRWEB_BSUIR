import numpy


class MatrixProcessor(object):

    def __init__(self, rows: int, cols: int):

        self.matrix = numpy.random.randint(-100, 100, size=(rows, cols))

    def process_matrix(self) -> numpy.ndarray:

        matrix = self.matrix.copy()  
    
        for i in range(matrix.shape[0]):
            if i >= matrix.shape[1]:  
                continue
            
            max_in_row_idx = numpy.argmax(numpy.abs(matrix[i]))
        
            matrix[i, i], matrix[i, max_in_row_idx] = matrix[i, max_in_row_idx], matrix[i, i]
    
        return matrix

    def compute_median(self) -> tuple[numpy.floating, float]:
    
        median_np = numpy.median(self.matrix)
    
        flattened = self.matrix.flatten()
        sorted_values = numpy.sort(flattened)
        n = len(sorted_values)
    
        if n % 2 == 1:
        
            median_manual = sorted_values[n // 2]
        else:
        
            median_manual = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    
        return median_np, float(median_manual)
