# -*- coding: utf-8 -*-
"""lab03-LocalSearch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CrgW4ppMP2GRIvfjv2T44q3CO1mUlA3J

Course: **Introduction to Artificial Intelligence** \
Lecturer: **Nguyen Thanh An** \
Lab 03: **Local Search**

Students implement Hill-Climbing Search, Local Beam Search, and Simulated Annealing Search algorithms following TODO 1 - 3. \
Students can add supporting attributes and methods to the three classes as needed.

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
        7 8
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

class LocalSearchStrategy:
  def search(self, g: Graph, src: int) -> tuple:
    '''
    return a tuple (u, p) in which
      u: the local maximum state
      p: the priority/weight/desirability/cost of u
    '''
    u=src
    p=g.H[u]
    for v,w in g.AL[u]:
      if g.H[v]+w>p:
        u=v
        p=g.H[v]+w
    return (u,p)

class HillClimbingSearch(LocalSearchStrategy):
  def search(self, g: Graph, src: int) -> tuple:
    '''
    return a tuple (u, p) in which
      u: the local maximum state
      p: the priority/weight/desirability/cost of u

    Note: weight of a node u = path_cost to u + heuristic value of u (similar to A*)
    '''
    u=src
    p=g.H[u]
    while True:
      if u not in g.AL:
        break
      for v,w in g.AL[u]:
        if g.H[v]+w>p:
          u=v
          p=g.H[v]+w
          break
      else:
        break
    return (u,p)
    

class LocalBeamSearch(LocalSearchStrategy):
  def search(self, g: Graph, src: int) -> tuple:
    '''
    return a tuple (u, p) in which
      u: the local maximum state
      p: the priority/weight/desirability/cost of u

    Note:
    - weight of a node u = path_cost to u + heuristic value of u (similar to A*)
    - parameter n is provided in the constructor
    '''
    states = [(g.H[src], src)]
    heapq.heapify(states)
    while states:
      p, u = heapq.heappop(states)
      if u not in g.AL:
        break
      for v, w in g.AL[u]:
        heapq.heappush(states, (p + w + g.H[v], v))
    return (u, p)



class SimulatedAnnealingSearch(LocalSearchStrategy):
  def search(self, g: Graph, src: int) -> tuple:
    '''
    return a tuple (u, p) in which
      u: the local maximum state
      p: the priority/weight/desirability/cost of u

    Note: schedule(t) = 1/(t^2) with t is the iteration step
    '''
    u = src
    p = g.H[u]
    t = 1
    while True:
      if u not in g.AL:
        break
      for v, w in g.AL[u]:
        if g.H[v] + w > p:
          u = v
          p = g.H[v] + w
          break
      else:
        for v, w in g.AL[u]:
          if g.H[v] + w > p - 1 / t ** 2:
            u = v
            p = g.H[v] + w
            break
        else:
          break
      t += 1
    return (u, p)
  
"""# Evaluation"""

hcs = HillClimbingSearch()
lbs = LocalBeamSearch()
sas = SimulatedAnnealingSearch()

for stg in [hcs, lbs, sas]:
  print(stg)
  u, p = stg.search(g, 0)
  print(u, p)

"""# Submission Notice


*   Maintain all cell outputs
*   Download and rename the notebook as **lab03_\<Student ID\>.ipynb**
*   Submit by the deadline

"""