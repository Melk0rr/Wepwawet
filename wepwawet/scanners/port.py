""" Port module adressing TCP/UDP port behaviour """


class Port:
  """ Port class """

  def __init__(self, port_number=80, application="Unknown", state = "open"):
    """ Constructor """
    if not isinstance(port_number, int):
      raise ValueError(f"Invalid port number: {port_number} !")
      
    self.number = port_number
    self.application = application
    self.state = state

  def get_number(self):
    """ Getter for port number """
    return self.number

  def get_application(self):
    """ Getter for application """
    return self.application

  def get_state(self):
    """ Getter for port open state """
    return self.state

  def set_number(self, number):
    """ Setter for port number """
    if isinstance(number, int):
      self.number = number

    else:
      raise ValueError(f"Invalid port number: {number} !")

  def set_state(self, new_state = "opened"):
    """ Setter for port open state """
    self.state = new_state

  def to_string(self):
    """ Returns a string based on port number and application """
    return f"{self.application}({self.number})"

  def to_dictionary(self):
    """ Returns a dictionary based on port number and application """
    return {"number": self.number, "application": self.application}
