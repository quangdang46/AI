# -*- coding: utf-8 -*-
"""lab02-BestFirstSearch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jQzyRuo_-RsLQjxS-rk3SZMcPlZItj3I

Course: **Introduction to Artificial Intelligence** \
Lecturer: **Nguyen Thanh An** \
Lab 02: **Best First Search**

Students implement GBFS and A* algorithms following TODO 1 - 2. \
Students can add supporting attributes and methods to the two classes as needed.

# Libraries
"""

import os
import heapq

"""# Graph class"""

# Directed, weighted graphs
class Graph:
  def __init__(self):
    self.AL = dict() # adjacency list
    self.V = 0
    self.E = 0
    self.H = dict()

  def __str__(self):
    res = 'V: %d, E: %d\n'%(self.V, self.E)
    for u, neighbors in self.AL.items():
      line = '%d: %s\n'%(u, str(neighbors))
      res += line
    for u, h in self.H.items():
      line = 'h(%d) = %d\n'%(u, h)
    return res

  def print(self):
    print(str(self))

  def load_from_file(self, filename):
    '''
        Example input file:
            V E
            u v w
            u v w
            u v w
            ...
            u1 h1
            u2 h2
            u3 h3
            ...

        # input.txt
        7 9
        0 1 5 
        0 2 6
        1 3 12
        1 4 9
        2 5 5
        3 5 8
        3 6 7
        4 6 4
        0 14
        1 13
        2 12
        3 11
        4 10
        5 9
        6 0
    '''
    if os.path.exists(filename):
      with open(filename) as g:
        self.V, self.E = [int(it) for it in g.readline().split()]
        for i in range(self.E):
          line = g.readline()
          u, v, w = [int(it) for it in line.strip().split()]
          if u not in self.AL:
            self.AL[u] = []
          self.AL[u].append((v, w))
        for i in range(self.V):
          line = g.readline()
          u, h = [int(it) for it in line.strip().split()]
          self.H[u] = h

g = Graph()
g.load_from_file('input.txt')
g.print()

"""# Search Strategies"""

class BestSearchStrategy:
  def search(self, g: Graph, src: int, dst: int) -> tuple:
    expanded = [] # list of expanded vertices in the traversal order
    path = [] # path from src to dst
    return expanded, path

class GBFS(BestSearchStrategy):
  def search(self, g: Graph, src: int, dst: int) -> tuple:
    expanded = [] # list of expanded vertices in the traversal order
    path = [] # path from src to dst
    if src not in g.AL or dst not in g.AL:
      return expanded, path
    queue = [(g.H[src], src)]
    visited = {src: None}

    while queue:
      _, u = heapq.heappop(queue)
      if u == dst:
        while u is not None:
          path.append(u)
          u = visited[u]
        path.reverse()
        return expanded, path
      for v, w in g.AL.get(u, []):
        if v not in visited:
          visited[v] = u
          heapq.heappush(queue, (g.H[v], v))
      expanded.append(u)

    return expanded, None



class AStar(BestSearchStrategy):
  def search(self, g: Graph, src: int, dst: int) -> tuple:
    expanded = [] # list of expanded vertices in the traversal order
    path = [] # path from src to dst
    if src not in g.AL or dst not in g.AL:
      return expanded, path
    queue = [(g.H[src], src)]
    visited = {src: None}
    cost = {src: 0}

    while queue:
      _, u = heapq.heappop(queue)
      if u == dst:
        while u is not None:
          path.append(u)
          u = visited[u]
        path.reverse()
        return expanded, path
      for v, w in g.AL.get(u, []):
        if v not in visited:
          visited[v] = u
          cost[v] = cost[u] + w
          heapq.heappush(queue, (cost[v] + g.H[v], v))
      expanded.append(u)

    return expanded, None
  

"""# Evaluation"""

gbfs = GBFS()
astar = AStar()

for stg in [gbfs, astar]:
  print(stg)
  expanded, path = stg.search(g, 0, g.V-1)
  print(expanded)
  print(path)

"""# Submission Notice


*   Maintain all cell outputs
*   Download and rename the notebook as **lab02_\<Student ID\>.ipynb**
*   Submit by the deadline

"""