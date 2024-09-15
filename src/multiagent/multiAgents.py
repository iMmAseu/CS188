# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import pdb

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # pdb.set_trace()
        return legalMoves[chosenIndex]

    # 注意参数之间的差距一定要偏小，因为曼哈顿距离之间的差距本来就很小，不然调整就是没有什么效果的
    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghost_dis_List = []

        for item in newGhostStates:
            int_ghost_state = tuple(int(x) for x in item.getPosition())
            g_distance = abs(newPos[0] - int_ghost_state[0]) + abs(newPos[1] - int_ghost_state[1])
            ghost_dis_List.append(g_distance)
            if newPos == int_ghost_state:
                return -5000

        dis_List = []

        for food in newFood.asList():
            distance = abs(newPos[0] - food[0]) + abs(newPos[1] - food[1])
            dis_List.append(distance)

        if dis_List:
            value = 50 - min(dis_List)
            if successorGameState.getScore() > 170 and successorGameState.getScore() < 250:
                value += 10
        else:
            value = 0

        if ghost_dis_List:
            g_value = max(ghost_dis_List)
            if g_value <= 2:
                g_value = 0
        else:
            g_value = 0

        # pdb.set_trace()
        return successorGameState.getScore() + value + g_value

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

# 注意只需要返回pacman的动作，不俗要返回幽灵的动作，所以记录一个动作即可
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState: GameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            else:
                # pdb.set_trace()
                v = -float('inf')
                legalmoves = gameState.getLegalActions(0)
                for action in legalmoves:
                    successorGameState = gameState.generateSuccessor(0, action)
                    v = max(v, min_value(successorGameState, depth - 1, gameState.getNumAgents() - 1))
                # pdb.set_trace()
                return v

        def min_value(gameState: GameState, depth, left_agent_num):
            # pdb.set_trace()
            if gameState.isWin() or gameState.isLose() or (depth == 0 and left_agent_num == 0):
                return self.evaluationFunction(gameState)
            else:
                v = float('inf')
                agent_index = gameState.getNumAgents() - left_agent_num
                legalmoves = gameState.getLegalActions(agent_index)
                for action in legalmoves:
                    successorGameState = gameState.generateSuccessor(agent_index, action)
                    if left_agent_num == 1:
                        v = min(v, max_value(successorGameState, depth))
                    else:
                        v = min(v, min_value(successorGameState, depth, left_agent_num - 1))
                # pdb.set_trace()
                return v

        depth = self.depth
        Value_List = []
        Action_List = gameState.getLegalActions(0)
        for action in Action_List:
            successorGameState = gameState.generateSuccessor(0, action)
            Value_List.append(min_value(successorGameState, depth - 1, gameState.getNumAgents() - 1))
        best = max(Value_List)
        Indices = [index for index in range(len(Value_List)) if Value_List[index] == best]
        chosenIndex = random.choice(Indices)
        # pdb.set_trace()
        return Action_List[chosenIndex]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState: GameState, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                # pdb.set_trace()
                return self.evaluationFunction(gameState)
            else:
                # pdb.set_trace()
                v = -float('inf')
                legalmoves = gameState.getLegalActions(0)
                for action in legalmoves:
                    successorGameState = gameState.generateSuccessor(0, action)
                    v = max(v, min_value(successorGameState, depth - 1, gameState.getNumAgents() - 1, alpha, beta))
                    if v > beta:
                        return v
                    alpha = max(alpha, v)
                # pdb.set_trace()
                return v

        def min_value(gameState: GameState, depth, left_agent_num, alpha, beta):
            if gameState.isWin() or gameState.isLose() or (depth == 0 and left_agent_num == 0):
                # pdb.set_trace()
                return self.evaluationFunction(gameState)
            else:
                v = float('inf')
                agent_index = gameState.getNumAgents() - left_agent_num
                legalmoves = gameState.getLegalActions(agent_index)
                for action in legalmoves:
                    # pdb.set_trace()
                    successorGameState = gameState.generateSuccessor(agent_index, action)
                    if left_agent_num == 1:
                        v = min(v, max_value(successorGameState, depth, alpha, beta))
                        if v < alpha:
                            return v
                        beta = min(beta, v)
                    else:
                        v = min(v, min_value(successorGameState, depth, left_agent_num - 1, alpha, beta))
                        if v < alpha:
                            return v
                        beta = min(beta, v)
                # pdb.set_trace()
                return v

        alpha = -float('inf')
        beta = float('inf')
        depth = self.depth
        Value_List = []
        Action_List = gameState.getLegalActions(0)
        # pdb.set_trace()
        for action in Action_List:
            successorGameState = gameState.generateSuccessor(0, action)
            v = min_value(successorGameState, depth - 1, gameState.getNumAgents() - 1, alpha, beta)
            Value_List.append(v)
            alpha = max(alpha, v)
        # pdb.set_trace()
        best = max(Value_List)
        Indices = [index for index in range(len(Value_List)) if Value_List[index] == best]
        chosenIndex = Indices[0]
        # pdb.set_trace()
        return Action_List[chosenIndex]
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
