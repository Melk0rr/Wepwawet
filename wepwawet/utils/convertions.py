from functools import reduce

def seconds_to_str(t):
  return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                                      [(t * 1000,), 1000, 60, 60])




def tuple_to_dictionnary(t, parent, res = {}):
  for a in t:
    print(f"a = {a}")
    #print(f"parent = {parent}")
    #if type(a) is tuple:
    #  return tuple_to_dictionnary(a, t,  res)
    #else:
    #  if type(a) is dict:
    #    res.append(a)  #parent[0][1] 
    #    print(res)
  return res



def tuple_to_dictionnaryold(t, parent, res = {}):
  for a in t:
    print(f"a = {a}")
    print(f"parent = {parent}")
    if type(a) is tuple:
      return tuple_to_dictionnary(a, t,  res)
    else:
      res[a] = parent[0][1] 
  return res


