# Name: Riya Dev
# Date: 12/2/2020
import os, time

###############
import random

def check_complete(assignment, csp_table):
   if assignment.find('.') != -1: return False
   for square in csp_table:
      if len(set([assignment[i] for i in square])) != 9: return False
   return True
   
def select_unassigned_var(assignment, variables, csp_table):
   #return random.choice([x for x in range(0, len(assignment)) if assignment[x] == "."]) #forward checking
   
   templist = [(len(variables[var]), var) for var in variables] #MRV
   #print(min(templist)[1])
   return min(templist)[1]
   #[(len(variables[var]), var) for var in variables ....]

def isValid(value, var_index, assignment, variables, csp_table):
   assignment = assignment[:var_index] + str(value) + assignment[var_index+1:]
   for x in csp_table: # [[0, 1, 2, 6, 7, 8], [2, 3, 4, 8, 9, 10], [5, 6, 7, 12, 13, 14], [7, 8, 9, 14, 15, 16], [9, 10, 11, 16, 17, 18], [13, 14, 15, 19, 20, 21], [15, 16, 17, 21, 22, 23]] 
      if var_index in x:
         for y in x: # [0, 1, 2, 6, 7, 8]
            if (not y == var_index) and (assignment[y] == assignment[var_index]): return False
               # print("Is Valid:", y, var_index, assignment[y], assignment[var_index])
   return True

def ordered_domain(assignment, variables, csp_table):
   return []

def update_variables(value, var_index, assignment, variables, csp_table): # make deepcopy to not update the fixed in variables
   temp = {k:{s for s in v} for k, v in variables.items() if k != var_index}
   for x in csp_table:
      if var_index in x:
         for y in x:
            if y in temp: temp[y] -= {value}
   return temp

def backtracking_search(puzzle, variables, csp_table): 
   return recursive_backtracking(puzzle, variables, csp_table)

def recursive_backtracking(assignment, variables, csp_table):
   if check_complete(assignment, csp_table): return assignment
   var_index = select_unassigned_var(assignment, variables, csp_table)
   
   #print(variables[var_index])
   for value in variables[var_index]: # csp_table[var_index]: #number
      tempvariables = update_variables(value, var_index, assignment, variables, csp_table)
      if isValid(value, var_index, assignment, variables, csp_table):
         assignmentcopy = assignment[:var_index] + str(value) + assignment[var_index + 1:]
         #print(tempvariables)
         
         result = recursive_backtracking(assignmentcopy, tempvariables, csp_table)
         if result != None: return result
         
   return None
   
def display(solution): # DONE
   result = ""
   for i in range(0, len(solution)):
      if i % 3 == 0 and i > 2: result += "  "
      if i % 9 == 0 and i > 8: result += '\n'
      if i % 27 == 0 and i > 26: result += '\n'
      result += solution[i] + " "
   return result

"""
def sudoku_csp():
   small_squares = []
   list = [0, 3, 6, 27, 30, 33]
   for x in list:
      small_squares.append([x, 1 + x, 2 + x, 9 + x, 10 + x, 11 + x, 18 + x, 19 + x, 20 + x])
      
   rows = []
   for x in range(0, 73, 9):
      rows.append([x, x + 1, x + 2, x + 3, x + 4, x + 5, x + 6, x + 7, x + 8])
      
   columns = []
   for x in range(0, 9):
      rows.append([x, x + 9, x + 18, x + 27, x +36, x + 45, x + 54, x + 63, x + 72])
   
   csp_table = []
   for x in small_squares:
      csp_table.append(x)
   for x in rows:
      csp_table.append(x)
   for x in columns:
      csp_table.append(x)

   return csp_table
"""

def initial_variables(puzzle):#, csp_table):
   variables = {}
   for x in range(0, len(puzzle)):
      if puzzle[x] == ".": variables[x] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
   return variables

###############

def solve(puzzle, neighbors): 
   #suggestion:
   # q_table is quantity table {'1': number of value '1' occurred, ...}
   # variables, puzzle, q_table = initialize_ds(puzzle, neighbors)  
   variables = initial_variables(puzzle)
   return recursive_backtracking(puzzle, variables, sudoku_csp())
   #return recursive_backtracking(puzzle, variables, neighbors, q_table)
   return None

def sudoku_neighbors(csp_table):
   # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   return {}
   
def sudoku_csp(n=9):
   csp_table = [[k for k in range(i*n, (i+1)*n)] for i in range(n)] # rows
   csp_table += [[k for k in range(i,n*n,n)] for i in range(n)] # cols
   temp = [0, 1, 2, 9, 10, 11, 18, 19, 20]
   csp_table += [[i+k for k in temp] for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]] # sub_blocks
   return csp_table

def checksum(solution):
   return sum([ord(c) for c in solution]) - 48*81 # One easy way to check a valid solution

def main():
   filename = input("file name: ")
   if not os.path.isfile(filename):
      filename = "puzzles.txt"
   csp_table = sudoku_csp()   # rows, cols, and sub_blocks
   neighbors = sudoku_neighbors(csp_table)   # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   start_time = time.time()
   for line, puzzle in enumerate(open(filename).readlines()):
      #if line == 50: break  # check point: goal is less than 0.5 sec
      line, puzzle = line+1, puzzle.rstrip()
      print ("Line {}: {}".format(line, puzzle)) 
      solution = solve(puzzle, neighbors)
      if solution == None:print ("No solution found."); break
      print ("{}({}, {})".format(" "*(len(str(line))+1), checksum(solution), solution))
   print ("Duration:", (time.time() - start_time))

if __name__ == '__main__': main()