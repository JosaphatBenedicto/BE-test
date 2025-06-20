"""
Item 1. 
Given a list of tuples A = (x, y), where x is an integer from 0 to 13 and y is an 
integer from 0 to 3, with all possible values of A without repetition and sorted 
by y then x in ascending order, write a pseudocode to shuffle A.
"""

"""
PSUEDOCODE:
import random module for shuffling

Function to shuffle the list of tuples A
function shuffle(list):
  shuffle the list with random.shuffle
  return shuffled list

if no shuffle function with the random module is available,
implement a custom shuffle function using Fisher-Yates algorithm
function shuffle_w_fisher_yates(list):
  for i in the range  of length of list - 1, down to 0:
    j = random index from 0 to i
    swap list[i] and list[j]
  return list

Function to call the shuffle function
function main():
  Construct list A, if not given`
  A = [(x, y) for x in range 0-13 and for y in range 0-3]
  shuffled_list = shuffle(A)
"""

from random import shuffle

def shuffle_tuples(tuples_list):
    #shuffle using the random module shufle function
    shuffle(tuples_list)
    return tuples_list

def main():
    # Original list of tuples A
    A = [(x, y) for x in range(14) for y in range(4)]
    
    # Shuffle the list
    shuffled_A = shuffle_tuples(A)
    
    # Print the shuffled result
    print(shuffled_A)

if __name__ == "__main__":
    main()
