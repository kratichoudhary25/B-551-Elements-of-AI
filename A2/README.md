#A2 Assignment

# Part 1

The problem is writing code for playing the raichu pieces efficiently in a checkers game with a few changes for the piece you choose by determining the best successor state to win by capturing all the pieces of the opponent.

Each player is given 3 kinds of pieces to play the game :-

- Pichu (w/b) : Can only move diagonally one space at a time if space is empty or jump over another pichu of the other player by moving two spaces forward.
- Pikachu(W/B) : Can move 1 or 2 spaces in forward, left or right to empty space or jump over 1 pichu or pikachu of opponent and move 2-3 spaces if the space after that is empty.
- Raichu(@/$) : Created when a pichu or pikachu reaches the opposite side of the board (black pichu or pikachu to row 1 or white pichu or pikachu to row n) and can move any number of spaces L,R,F,B or diagonally as long as there are no pieces in between or the places before and after the jumped piece are empty. 

Here, w- white pichu, W- white pikachu, b- black pichu, B-black pikachu, @- white raichu, $- black raichu, "."- places with no piece 

All jumped pieces are removed immediately.

## Order
First raichu, then pikachu, then pichu will have the power of order. When it comes to maintaining order, Pichu is least powerful.

## How to decide who's the winner?
So amongst black and white, the winners would be the ones who succeeds in capturing the all peices of the opponent players. 

## Implementation of the program
- We have implementated the Minmax algorithm to determine the best moves or maximum value from all of its succeeding states, which then determined the     minimal value from its succeeding states.
- Created every potential successor that could be produced.
- Gathered all potential successors and their evaluation rates in one place.
- Based on the disparity in material scores between our player and the opponent player, we used an evaluation function in this case.
- Depending on how many moves they can play on an empty board, different piece weights could be assigned. Here we have assigned 6 moves to pikachu. 
- Our program's mobility function provides us with the number of legal moves and errors.
- The material score was calculated by multiplying these weights by the variances across components of the same kind and the mobility function.



# Part 2

## AIM
- Aim of the part is to classify the objects into two categories truth and deceptive.     

## Implementation of the program
- In classfier definition, we are trying to check the occurances of truth/deceptive.  
 - With train data we have calulated the number of occurances of truthfulness and deceptiveness and stored the count value for the word by manitaing a dictionary.
- With the test data we had calculated the probabilty for truthfulness and deceptiveness, Where we have handled few edge cases of probablity getting '0' if the words are not found.
- And then calculating the probability of the review in test data being deceptive or truthful. 
- Then returning the value if probability is greater than 1 for truth else deceptive. 
- In the main function , classifer function is used inorder to calculate the accuracy, the classification accuracy is displayed.



