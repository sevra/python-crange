#!/usr/bin/env python

try: from itertools import izip_longest as zip_longest
except ImportError: from itertools import zip_longest

class Crange(tuple):
   '''
   Instances of Crange can return range generators based on the iterable 'items'.
   The default range returned is from the first index of 'items' to the last index
   of 'items'. 'items' defaults to 'abcdefghijklmnopqrstuvwxyz'.
   '''
   def __new__(self, start=None, stop=None, min=1, items='abcdefghijklmnopqrstuvwxyz'):
      self = tuple.__new__(Crange, items)

      self.items = items
      self.len = len(self)-1
      self.min = min if min > 1 else 1

      start = start if start else [self[0]]
      self.start = list(map(self.index, start))
      
      stop = stop if stop else [self[self.len]]
      self.stop = list(map(self.index, stop))
      
      while len(self.start) < min:
         self.start.append(0)

      while len(self.stop) <  min:
         self.stop.append(self.len)

      return self

   def range(self, start=None, stop=None, min=1):
      '''
      Returns a copy of the original object with a new range.
      '''
      return Crange(start, stop, min, self.items)

   def __iter__(self):
      start = self.start
      stop = self.stop
      min = self.min
      
      cur = list(start)
      i = (len(cur)-1)

      def index_cmp(*args, **kargs):
         fill = kargs.get('fill', None)
         count = 0
         for items in zip_longest(*args, fillvalue=fill):
            if len(set(items)) > 1:
               return count
            count += 1
         return -1

      y_triggered = False
      while cur <= stop or index_cmp(stop, cur) == len(stop):
      # continue yielding values if cur is less than or equal to stop
      # or if the index stop and cur differ on is the same 
         x = index_cmp(start, cur)
         if x >= min-1 and not len(cur)-1 == x and not y_triggered: 
         # if the index that 'start' and 'cur' differ on (x), is less
         # than the zero based index value of 'min' (min-1) then we
         # shall reduce the size of cur.
            i = x
            cur = cur[:i+1]
            # modifying the length of 'cur' is necessary to ensure that
            # the list comparison in the encompasing 'while' loop
            # works correctly. 
         
         y = index_cmp(stop, cur)
         if y > i and not len(cur)-1 == y:
            y_triggered = True
            while index_cmp(cur, stop[:i+1]) == -1 and len(cur) < len(stop):
            # while 'cur' and 'stop from 0 to i' match and the length of 'cur'
            # is less than the length of 'stop', increase the size of 'cur'
            # by one.
               i += 1
               cur.append(0)
               # the same as the above comment about modifying the length
               # of 'cur'.

         yield [str(self[c]) for c in cur]

         if cur[i] < self.len:
            cur[i] += 1
         elif cur[i] == self.len:
            cur[i] = 0
            for j in reversed(range(0, i)):
               if cur[j] == self.len:
                  cur[j] = 0
               elif cur[j] < self.len:
                  cur[j] += 1
                  break
            else:
               break

if __name__ == '__main__':
   try:   
      from itertools import product

      alpha = Crange()
      num = Crange(items=[0, 1, 2, 3, 4])

      def run(start, stop, min=0, items=alpha):
         print('Running "%s" to "%s" with a min of "%s"' % (start, stop, min))
         for x in items.range(start, stop, min):
            print(x)
         print('Ran "%s" to "%s" with a min of "%s"' % (start, stop, min))
         input()
   
      run([0, 1], [4, 2], min=3, items=num)
      run('a', 'cbac')
      run('rx', 's')
      run(None, None)
      run('h', 'laotzu')
   
      starts = ('r', 'rx', 'rxn'); stops = ('t', 'tu', 'tuv'); mins = (1, 2, 3)
      for (start, stop, min) in product(starts, stops, mins):
         run(start, stop, min)

      for x in alpha.range('ggzz', 'i'):
         print(x)
         if ''.join(x) == 'gh':
            for z in (x + y for y in alpha.range()):
               print(z)
      input()

      for x in alpha.range('ggue', 'i'):
         print(x)
         if ''.join(x) == 'h':
            for z in (x + y for y in alpha.range()):
               print(z)
      input()

   except KeyboardInterrupt:
      raise SystemExit()

# vim: set foldmethod=manual:
