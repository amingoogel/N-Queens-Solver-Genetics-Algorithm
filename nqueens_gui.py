class NQueensGUI:
    """
    GUI implementation for the N-Queens solver
    """
    def __init__(self, root):
        """
        Initialize the GUI
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("N-Queens Genetic Algorithm Solver")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input parameters
        ttk.Label(self.main_frame, text="Board Size (N):").grid(row=0, column=0, sticky=tk.W)
        self.n_var = tk.StringVar(value="8")
        self.n_entry = ttk.Entry(self.main_frame, textvariable=self.n_var, width=10)
        self.n_entry.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.main_frame, text="Population Size:").grid(row=1, column=0, sticky=tk.W)
        self.pop_size_var = tk.StringVar(value="100")
        self.pop_size_entry = ttk.Entry(self.main_frame, textvariable=self.pop_size_var, width=10)
        self.pop_size_entry.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(self.main_frame, text="Generations:").grid(row=2, column=0, sticky=tk.W)
        self.generations_var = tk.StringVar(value="100")
        self.generations_entry = ttk.Entry(self.main_frame, textvariable=self.generations_var, width=10)
        self.generations_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Solve button
        self.solve_button = ttk.Button(self.main_frame, text="Solve", command=self.solve)
        self.solve_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=2)
        
        # Canvas for board
        self.canvas = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10)
        
    def draw_board(self, solution):
        """
        Draw the chess board and queens
        Args:
            solution: List representing queen positions
        """
        self.canvas.delete("all")
        n = len(solution)
        cell_size = 400 // n
        
        # Draw checkerboard pattern
        for i in range(n):
            for j in range(n):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "#FFFFFF" if (i + j) % 2 == 0 else "#CCCCCC"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        
        # Draw queens as red circles
        for i, j in enumerate(solution):
            x = j * cell_size + cell_size // 2
            y = i * cell_size + cell_size // 2
            radius = cell_size // 3
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                  fill="red", outline="black")
    
    def solve(self):
        """Handle the solve button click event"""
        try:
            # Get input parameters
            n = int(self.n_var.get())
            pop_size = int(self.pop_size_var.get())
            generations = int(self.generations_var.get())
            
            # Validate input
            if n < 4:
                self.status_var.set("N must be at least 4")
                return
                
            self.status_var.set("Solving...")
            self.root.update()
            
            # Run the genetic algorithm
            solver = NQueensGA(n, pop_size, generations)
            solution, fitness = solver.evolve()
            
            # Display results
            if fitness == 0:
                self.status_var.set(f"Solution found! Conflicts: {fitness}")
                self.draw_board(solution)
            else:
                self.status_var.set(f"No perfect solution found. Best conflicts: {fitness}")
                self.draw_board(solution)
                
        except ValueError:
            self.status_var.set("Invalid input values")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
