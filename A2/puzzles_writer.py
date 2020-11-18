import os

class PuzzlesWriter:
    """Write puzzle <solution/search path> to given file."""
    
    output_files_path = "output_files/"
    
    output_types = ["solution", "search"]
    
    file_output_format = "{}_{}_{}.txt"
    
    def __init__(self, puzzle_number, algo_name, solution, search):
        os.makedirs(os.path.dirname(self.output_files_path), exist_ok=True)

        file_name_solution = self.file_output_format.format(puzzle_number, algo_name, self.output_types[0])
        file_solution = open(self.output_files_path + file_name_solution, "w")
        file_solution.write(solution)
        file_solution.close()
        
        file_name_search = self.file_output_format.format(puzzle_number, algo_name, self.output_types[1])
        file_search = open(self.output_files_path + file_name_search, "w")
        file_search.write(search)
        file_search.close()