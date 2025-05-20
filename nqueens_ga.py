import random  # For random operations
import numpy as np  # For numerical operations

class NQueensGA:
    """
    Genetic Algorithm implementation for solving the N-Queens problem
    """
    def __init__(self, n=8, population_size=100, generations=100):
        """
        Initialize the genetic algorithm solver
        Args:
            n: Size of the chess board (n x n)
            population_size: Number of solutions in each generation
            generations: Maximum number of generations to evolve
        """
        self.n = n
        self.population_size = population_size
        self.generations = generations
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
        
    def initialize_population(self):
        """Initialize the population with random solutions"""
        self.population = []
        for _ in range(self.population_size):
            solution = list(range(self.n))
            random.shuffle(solution)  # Randomly place queens
            self.population.append(solution)
            
    def fitness(self, solution):
        """
        Calculate the fitness of a solution (number of conflicts)
        Lower fitness is better (0 means no conflicts)
        """
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Check diagonal conflicts
                if abs(i - j) == abs(solution[i] - solution[j]):
                    conflicts += 1
        return conflicts
    
    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to create a child
        Uses single-point crossover
        """
        point = random.randint(0, self.n - 1)
        child = [-1] * self.n
        child[:point] = parent1[:point]
        
        # Fill remaining positions with unused values from parent2
        remaining = [x for x in parent2 if x not in child[:point]]
        child[point:] = remaining
        
        return child
    
    def mutate(self, solution):
        """
        Randomly swap two positions in the solution
        Mutation rate is 10%
        """
        if random.random() < 0.1:  # 10% mutation rate
            i, j = random.sample(range(self.n), 2)
            solution[i], solution[j] = solution[j], solution[i]
        return solution
    
    def select_parent(self):
        """
        Tournament selection to choose a parent
        Selects the best solution from a random tournament
        """
        tournament_size = 5
        tournament = random.sample(self.population, tournament_size)
        return min(tournament, key=self.fitness)
    
    def evolve(self):
        """
        Main evolution loop
        Returns the best solution found and its fitness
        """
        self.initialize_population()
        
        for generation in range(self.generations):
            new_population = []
            
            # Elitism: Keep the best solution
            best_solution = min(self.population, key=self.fitness)
            new_population.append(best_solution)
            
            # Create new population
            while len(new_population) < self.population_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            
            self.population = new_population
            
            # Update best solution
            current_best = min(self.population, key=self.fitness)
            current_fitness = self.fitness(current_best)
            
            if current_fitness < self.best_fitness:
                self.best_solution = current_best.copy()
                self.best_fitness = current_fitness
                
            # Stop if perfect solution found
            if self.best_fitness == 0:
                break
                
        return self.best_solution, self.best_fitness
    #finshed

