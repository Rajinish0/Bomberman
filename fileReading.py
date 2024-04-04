class GridReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.grid = []

    def read_grid(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                self.grid.append(list(line.strip()))

    def get_grid(self):
        return self.grid