# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import pdb

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# 以下的所有算法要注意两点：
# 需要记录路径，因为可能会用到
# 每个节点的状态应该同时包括是否达成目标（针对q5），这样才能保证可以回头
# dfs寻找路径速度快，但不保证最优
def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    exploreNodes = set()
    fringe = util.Stack()

    if (problem.isGoalState(problem.getStartState())):
        return Directions.STOP
    fringe.push([(problem.getStartState(), 'Start', 0)])

    while not fringe.isEmpty():
        currentPath = fringe.pop()
        currentState = currentPath[-1][0]
        if currentState in exploreNodes:
            continue
        if (problem.isGoalState(currentState)):
            break
        successors = problem.getSuccessors(currentState)
        for x in successors:
            if x[0] not in exploreNodes:
                # 此处使用浅拷贝
                nextPath = currentPath[:]
                nextPath.append(x)
                fringe.push(nextPath)
        exploreNodes.add(currentState)

    return [x[1] for x in currentPath[1:]]

    # from game import Directions
    # s = Directions.SOUTH
    # n = Directions.NORTH
    # w = Directions.WEST
    # e = Directions.EAST
    #
    # start = problem.getStartState()
    # pos_stack = util.Stack()
    # dir_stack = util.Stack()
    # result_stack = util.Stack()
    # closer = set()
    #
    # # 初始化
    # pos_stack.push(start)
    # pos = pos_stack.list[-1]
    #
    # while True:
    #     if problem.isGoalState(pos):
    #         return result_stack.list
    #     elif pos in closer:
    #         dir_stack.pop()
    #         pos_stack.pop()
    #         pos = pos_stack.list[-1]
    #         result_stack.pop()
    #         if pos not in closer:
    #             result_stack.pop()
    #             result_stack.push(dir_stack.list[-1])
    #     else:
    #         closer.add(pos)
    #         expand = problem.getSuccessors(pos)
    #         for item in expand:
    #             (position, direction, value) = item
    #             if position not in closer:
    #                 pos_stack.push(position)
    #                 dir_stack.push(direction)
    #         pos = pos_stack.list[-1]
    #         result_stack.push(dir_stack.list[-1])

    # pdb.set_trace()
    # util.raiseNotDefined()

# bfs在无权图中可以保证最优
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    exploreNodes = set()
    fringe = util.Queue()

    if(problem.isGoalState(problem.getStartState())):
        return Directions.STOP
    fringe.push([(problem.getStartState(), 'Start', 0)])

    while not fringe.isEmpty():
        currentPath = fringe.pop()
        currentState = currentPath[-1][0]
        if currentState in exploreNodes:
            continue
        if (problem.isGoalState(currentState)):
            break
        successors = problem.getSuccessors(currentState)
        for x in successors:
            if x[0] not in exploreNodes:
                # 此处使用浅拷贝
                nextPath = currentPath[:]
                nextPath.append(x)
                fringe.push(nextPath)
        exploreNodes.add(currentState)

    return [x[1] for x in currentPath[1:]]

    # # 初始化
    # pos_queue.push(start)
    # pos = pos_queue.pop()
    #
    # while True:
    #     path = []
    #     for now_path in path_all:
    #         if pos == now_path[-1]:
    #             # 注意一定使用浅拷贝
    #             path = list(now_path)
    #     pdb.set_trace()
    #     if problem.isGoalState((pos, path)):
    #         while pos != start:
    #             result.append(predecessors[pos][1])
    #             pos = predecessors[pos][0]
    #         result.reverse()
    #         return result
    #     elif pos in closer:
    #         pos = pos_queue.pop()
    #     else:
    #         closer.add(pos)
    #         expand = problem.getSuccessors((pos, []))
    #         for item in expand:
    #             (position, direction, value) = item
    #             # 注意这里必须确保第一次的前驱不被覆盖，否则得到的结果不是最优的
    #             # 正确的写法是使用
    #             if position not in closer:
    #                 path.append(position)
    #                 path_all.append(list(path))
    #                 path.pop()
    #                 if position not in predecessors:
    #                     pos_queue.push(position)
    #                     predecessors[position] = (pos, direction)
    #         # pdb.set_trace()
    #         pos = pos_queue.pop()



    # pdb.set_trace()
    # util.raiseNotDefined()

# 为什么ucs和bfs回溯节点的方法不一样？这是因为bfs的每条路径的代价都是1，所以不会出现路径短，但是代价反而高的这种情况
# 这时只要粗暴地选择保留先加入字典的回溯路径就可以保证一定能找到最短路径，而统一代价搜索则不同，他可能需要选择一些路径数长，但是总代价小的路径
# 可以看这两个例子加深理解
#              B1          E1
#             ^  \        ^  \
#            /    V      /    V
#          *A --> C --> D --> F --> [G]
#            \    ^      \    ^
#             V  /        V  /
#              B2          E2
#
#             1      1      1
#          *A ---> B ---> C ---> [G]
#           |                     ^
#           |         10          |
#           \---------------------/


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    exploreNodes = set()
    fringe = util.PriorityQueue()

    if (problem.isGoalState(problem.getStartState())):
        return Directions.STOP
    fringe.push([(problem.getStartState(), 'Start', 0)], 0)

    while not fringe.isEmpty():
        currentPath = fringe.pop()
        currentState = currentPath[-1][0]
        if currentState in exploreNodes:
            continue
        if (problem.isGoalState(currentState)):
            break
        successors = problem.getSuccessors(currentState)
        for x in successors:
            if x[0] not in exploreNodes:
                # 此处使用浅拷贝
                nextPath = currentPath[:]
                nextPath.append(x)
                cost = 0
                for y in nextPath:
                    cost += y[2]
                fringe.push(nextPath, cost)
        exploreNodes.add(currentState)

    return [x[1] for x in currentPath[1:]]

    # from game import Directions
    # s = Directions.SOUTH
    # n = Directions.NORTH
    # w = Directions.WEST
    # e = Directions.EAST
    #
    # start = problem.getStartState()
    # pos_heap = util.PriorityQueue()
    # predecessors = {}
    # closer = set()
    # result = []
    #
    # pos_heap.push(start, 0)
    # pos = pos_heap.pop()
    #
    # while True:
    #     if problem.isGoalState(pos):
    #         while pos != start:
    #             result.append(predecessors[pos][1])
    #             pos = predecessors[pos][0]
    #         result.reverse()
    #         return result
    #     elif pos in closer:
    #         pos = pos_heap.pop()
    #     else:
    #         closer.add(pos)
    #         expand = problem.getSuccessors(pos)
    #         for item in expand:
    #             (position, direction, value) = item
    #             if position not in closer:
    #                 old_value = float('inf')
    #                 if position in predecessors:
    #                     (old_pos, old_direction, old_value) = predecessors[position]
    #                 predecessors[position] = (pos, direction, value)
    #                 now = position
    #                 cost = 0
    #                 while now != start:
    #                     cost += predecessors[now][2]
    #                     now = predecessors[now][0]
    #                 #  出现重复的节点时，回溯并比较权重得出答案
    #                 if old_value < cost:
    #                     predecessors[position] = (old_pos, old_direction, old_value)
    #                 pos_heap.push(position, cost)
    #         pos = pos_heap.pop()

    # pdb.set_trace()
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# 如果使用两个数组分别存放之前的路径的消耗和之前的节点预计消耗及路径消耗之和，记得节点重复时对两个字典都进行更换
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # from game import Directions
    # s = Directions.SOUTH
    # n = Directions.NORTH
    # w = Directions.WEST
    # e = Directions.EAST
    #
    # start = problem.getStartState()
    # pos_heap = util.PriorityQueue()
    # predecessors_path = {}
    # predecessors = {}
    # closer = set()
    # result = []
    #
    # pos_heap.push(start, 0)
    # pos = pos_heap.pop()
    #
    # while True:
    #     if problem.isGoalState(pos):
    #         while pos != start:
    #             result.append(predecessors[pos][1])
    #             pos = predecessors[pos][0]
    #         result.reverse()
    #         return result
    #     elif pos in closer:
    #         pos = pos_heap.pop()
    #     else:
    #         closer.add(pos)
    #         expand = problem.getSuccessors(pos)
    #         for item in expand:
    #             (position, direction, value) = item
    #             if position not in closer:
    #                 old_value = float('inf')
    #                 if position in predecessors:
    #                     (old_pos, old_direction, old_value) = predecessors[position]
    #                     (old_pos_path, old_direction_path, old_value_path) = predecessors_path[position]
    #                 predecessors_path[position] = (pos, direction, value)
    #                 now = position
    #                 h = heuristic(now, problem)
    #                 cost = h
    #                 while now != start:
    #                     cost += predecessors_path[now][2]
    #                     now = predecessors_path[now][0]
    #                 #  出现重复的节点时，回溯并比较权重得出答案
    #                 if old_value < cost:
    #                     predecessors[position] = (old_pos, old_direction, old_value)
    #                     predecessors_path[position] = (old_pos_path, old_direction_path, old_value_path)
    #                 else:
    #                     predecessors[position] = (pos, direction, cost)
    #                 pos_heap.push(position, cost)
    #         pos = pos_heap.pop()

    from game import Directions
    exploreNodes = set()
    fringe = util.PriorityQueue()

    if (problem.isGoalState(problem.getStartState())):
        return Directions.STOP
    fringe.push([(problem.getStartState(), 'Start', 0)], heuristic(problem.getStartState(), problem))

    while not fringe.isEmpty():
        currentPath = fringe.pop()
        currentState = currentPath[-1][0]
        if currentState in exploreNodes:
            continue
        if (problem.isGoalState(currentState)):
            break
        successors = problem.getSuccessors(currentState)
        for x in successors:
            if x[0] not in exploreNodes:
                # 此处使用浅拷贝
                nextPath = currentPath[:]
                nextPath.append(x)
                cost = heuristic(x[0], problem)
                for y in nextPath:
                    cost += y[2]
                fringe.push(nextPath, cost)
        exploreNodes.add(currentState)

    return [x[1] for x in currentPath[1:]]

        # pdb.set_trace()
        # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
