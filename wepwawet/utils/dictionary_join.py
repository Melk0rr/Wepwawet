"""
  Join dictionary items with the provided character
"""
def join_dictionary(dictionary, char):
  return char.join('{} : {}'.format(k, v) for k, v in dictionary.items())