# krachoud-a0

# Question 1

Beginning State: Input map

Goal State: Shortest route from start point to end point

Successor Function: Every valid space in the input map until pichu reaches destination

Approach: For the first problem, we had to implement search algorithm to look for the most efficient way to reach from one point to another. I used a pretty straightforward approach called Breadth First Search implemented with a stack. There is a visited list which stores all the unique nodes that were visited while exploring all the child nodes of a parent node (next adjacent nodes available for traversal) while checking if the next traversing node is the destination. If the pichu hits a place where it can't move forward, it will traverse back to the previous node where it came from and look for other directions to go (revert back to parent node and look for other child nodes). It keeps repeating this process until it either doesn't have a place to look for or it reaches the destination. 

# Question 2

Beginning State: Input Map

Goal State: Arranging pichus such that there is no pichu in other pichu's sight

Approach: The second problem looked like a modified version of the n-Queens problem that is solved by backtracking. The process started by looking for the first valid position to place a pichu and then to add more pichus. It places a pichu at a particular coordinate and then checks the row, column, and all 4 diagonal directions of the pichu for you, any other pichus, and walls places it at that coordinate if the position is valid or keeps travering until it finds a valid place. Then this function is passed to another function which generates the updated map.
