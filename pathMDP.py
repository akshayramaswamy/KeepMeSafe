class SafePathMDP(util.MDP):
    def __init__(self, locationGrid, startRow, startCol, endRow, endCol):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.locationGrid = locationGrid
        self.row = startRow
        self.col = startCol
        self.endRow = endRow
        self.endCol = endCol

    # Return the start state.
    # State represented as: (curr row, curr col, # of edges currently traversed, total sum of rewards)
    def startState(self):
        return (self.row, self.col, 0, 0)

    # Given a list of valid actions, remove all actions that take you to a visited square in the grid
    def getUnvisitedActions(self, actions):
        if "U" in actions:
            if self.locationGrid[row - 1][col][2]:
                actions.remove("U")

        if "D" in actions:
            if self.locationGrid[row + 1][col][2]:
                actions.remove("D")

        if "L" in actions:
            if self.locationGrid[row][col - 1][2]:
                actions.remove("L")

        if "R" in actions:
            if self.locationGrid[row][col + 1][2]:
                actions.remove("R")

        if "UL" in actions:
            if self.locationGrid[row - 1][col - 1][2]:
                actions.remove("UL")

        if "UR" in actions:
            if self.locationGrid[row - 1][col + 1][2]:
                actions.remove("UR")

        if "DL" in actions:
            if self.locationGrid[row + 1][col - 1][2]:
                actions.remove("DL")

        if "DR" in actions:
            if self.locationGrid[row + 1][col + 1][2]:
                actions.remove("DR")

        return actions

    # Return set of actions possible from |state|.
    # Can go up, down, left, right, up-right, up-left, down-right, down-left
    # CANNOT GO TO VISITED PLACES - DO THIS
    def actions(self, state):
        row = state[0]
        col = state[1]
        # Find the special case actions - on boundary of grid
        if row == 0 or row == len(self.locationGrid) - 1 or col == 0 or col == len(self.locationGrid[0]) - 1:
            # Top Left Corner
            if row == 0 and col == 0:
                return getUnvisitedActions(["D", "R", "DR"])

            # Top Right Corner
            if row == 0 and col == len(self.locationGrid[0]) - 1:
                return getUnvisitedActions(["D", "L", "DL"])

            # Bottom Left Corner
            if row == len(self.locationGrid) - 1 and col == 0:
                return getUnvisitedActions(["U", "R", "UR"])

            # Bottom Right Corner
            if row == len(self.locationGrid) - 1 and col == len(self.locationGrid[0]) - 1:
                return getUnvisitedActions(["U", "R", "UR"])

            # Top row
            if row == 0:
                return getUnvisitedActions(["D", "L", "R", "DL", "DR"])

            # Bottom row
            if row == len(self.locationGrid) - 1:
                return getUnvisitedActions(["U", "L", "R", "UL", "UR"])

            # Left col
            if col == 0:
                return getUnvisitedActions(["U", "D", "R", "UR", "DR"])

            # Right Col
            if col == len(self.locationGrid[0]) - 1:
                return getUnvisitedActions(["U", "D", "L", "UL", "DL"])

        # Otherwise explore all 8 possible actions
        return getUnvisitedActions(["U", "D", "L", "R", "UL", "UR", "DL", "DR"])

    def isEnd(self, row, col):
        return row == self.endRow and col == self.endCol

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        row, col, numEdges, sumRewards = state
        prob = 1

        # Set state as visited
        self.locationGrid[newRow][newCol][2] = True

        # End state: reached destination
        if row == self.endRow and col == self.endCol:
            return []

        # Up action
        if action == "U":
            newRow = row - 1
            newCol = col
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Down action
        if action == "D":
            newRow = row + 1
            newCol = col
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Left action
        if action == "L":
            newRow = row
            newCol = col - 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Right action
        if action == "R":
            newRow = row
            newCol = col + 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Up-left action
        if action == "UL":
            newRow = row - 1
            newCol = col - 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Up-right action
        if action == "UR":
            newRow = row - 1
            newCol = col + 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Down-left action
        if action == "DL":
            newRow = row + 1
            newCol = col - 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

        # Down-right action
        if action == "DR":
            newRow = row + 1
            newCol = col + 1
            newNumEdges = numEdges + 1
            newSumRewards = sumRewards + self.locationGrid[newRow][newCol][1]
            newState = (newRow, newCol, newNumEdges, newSumRewards)
            if self.isEnd(newRow, newCol):
                reward = newSumRewards / (float) (newNumEdges)
            else:
                reward = 0
            return [(newState, prob, reward)]

    def discount(self):
        return 1