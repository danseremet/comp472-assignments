class PuzzlesReader:
    """Read input puzzles from given file."""
    
    def __init__(self, path):
        file = open(path, "r")
        puzzleLines = file.read().split("\n")
        self.puzzles = []
        
        for i in range(0, len(puzzleLines)):
            puzzle = puzzleLines[i].split()
            self.puzzles.append(puzzle)