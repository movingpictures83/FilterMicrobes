import sys
import numpy
import random
import Queue

# Scaling is done to make median=1
class FilterMicrobesPlugin:
   def input(self, filename):
      self.myfile = filename

   def run(self):
      filestuff = open(self.myfile, 'r')
      # Use first file to get indices
      self.firstline = filestuff.readline().strip()
      lines = []
      for line in filestuff:
         lines.append(line.strip())

      self.m = len(lines)
      self.samples = []
      self.bacteria = self.firstline.split(',')
      if (self.bacteria.count('\"\"') != 0):
         self.bacteria.remove('\"\"')

      # Note assumes microbes, followed by metabolites
      metaboliteIndex = -1
      for i in range(len(self.bacteria)):
         print self.bacteria[i]
         if (self.bacteria[i][1] == 'X' and self.bacteria[i][2].isdigit()):
            metaboliteIndex = i
            break
      print "METABOLITEINDEX: ", metaboliteIndex

      # Assemble adjacency matrix as normal
      self.n = len(self.bacteria)
      self.ADJ = []#numpy.zeros([self.m, self.n])
      self.ADJ2 = []
      i = 0
      print "M: ", self.m
      print "N: ", self.n
      for i in range(self.m):
            self.ADJ.append([])
            self.ADJ2.append([])
            contents = lines[i].split(',')
            self.samples.append(contents[0])
            for j in range(self.n):
               #print contents[j+1]
               value = float(contents[j+1].strip())
               #print self.ADJ[i][j]
               self.ADJ[i].append(value)#[j] = value
               self.ADJ2[i].append(value)
            i += 1

      # Zero out all microbe-microbe interactions
      for i in range(0, metaboliteIndex):
         for j in range(0, metaboliteIndex):
            if (i != j):
               self.ADJ2[i][j] = 0
         for j in range(metaboliteIndex, len(self.ADJ2[i])):
            self.ADJ2[i][j] = self.ADJ[i][j]
      for i in range(metaboliteIndex, self.n):
         for j in range(0, self.n):
            self.ADJ2[i][j] = self.ADJ[i][j]

      # Keep any microbe-microbe interactions with some path between them
      # involving NO microbe-microbe edges.
      # Build iteratively until no more changes are necessary
      flag = False
      while (not flag):
         flag = True
         for i in range(0, metaboliteIndex):
            for j in range(0, metaboliteIndex):
               #print "CHECKING ", i, " AND ", j, ":",
               if (self.ADJ[i][j] != 0 and self.ADJ2[i][j] == 0 and self.isReachable(i, j)):
                  print "PUTTING BACK ", i, " ", j
                  self.ADJ2[i][j] = self.ADJ[i][j]
                  self.ADJ2[j][i] = self.ADJ2[j][i]
                  flag = False
 
      for i in range(self.m):
         for j in range(self.n):
            self.ADJ[i][j] = self.ADJ2[i][j]     
      
  
   def output(self, filename):
      filestuff2 = open(filename, 'w')
      filestuff2.write(self.firstline+"\n")
      
      for i in range(self.m):
         filestuff2.write(self.samples[i]+',')
         for j in range(self.n):
            filestuff2.write(str(self.ADJ[i][j]))
            if (j < self.n-1):
               filestuff2.write(",")
            else:
               filestuff2.write("\n")


   def isReachable(self, s, d):
      if (s == d):
         return True
      else:
         visited = []
         for i in range(0, self.n):
            visited.append(False)

         queue = Queue.Queue()
         visited[s] = True
         queue.put(s)

         while (not queue.empty()):
            s = queue.get()
            for i in range(len(self.ADJ2[s])):
               if (self.ADJ2[s][i] != 0):
                  if (i == d):
                     return True
                  else:
                     if (not visited[i]):
                        visited[i] = True
                        queue.put(i)

      return False

