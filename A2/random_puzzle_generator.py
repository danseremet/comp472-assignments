lshw -c displayimport os
import numpy as np

class RandomPuzzleGenerator:
    def generate_random_puzzle(self, rows, cols):
        puzzles = np.arange(1, rows * cols + 1).reshape(rows, cols)
        puzzles[-1][-1] = 0
        puzzles = np.array(puzzles)
        puzzles = np.vectorize(str)(puzzles)
        puzzles = puzzles.reshape(1, rows * cols)
        puzzles = list(puzzles[0])
        np.random.shuffle(puzzles)
        puzzles = " ".join(puzzles)
        return puzzles
    
    def __init__(self):
#         puzzles = []

        puzzles2x4 = []
        puzzles3x4 = []
        puzzles4x4 = []
        for i in range(3):  
            puzzles2x4.append(self.generate_random_puzzle(2, 4))
            puzzles3x4.append(self.generate_random_puzzle(3, 4))
            puzzles4x4.append(self.generate_random_puzzle(4, 4))
        
        puzzles2x4 = "\n".join(puzzles2x4)
        puzzles3x4 = "\n".join(puzzles3x4)
        puzzles4x4 = "\n".join(puzzles4x4)
            
        puzzles = [puzzles2x4, puzzles3x4, puzzles4x4]
#         puzzles = "\n".join(puzzles)
        
        print(puzzles)
        files = [
            "random_5_2x4_puzzles.txt", 
            "random_5_3x4_puzzles.txt", 
            "random_5_4x4_puzzles.txt"
        ]

        for i, file in enumerate(files):
            f = open(file, "w")
            f.write(puzzles[i])
            f.close()    
        
#         file = open("random_50_puzzles.txt", "w")
#         file.write(puzzles)
#         file.close()
        
def main():
    RandomPuzzleGenerator()

if __name__ == "__main__":
    main()
