class A(object):
  def __init__(self):
   print "enter A"
   super(A, self).__init__()  # new
   print "leave A"

class B(object):
  def __init__(self):
   print "enter B"
   super(B, self).__init__()  # new
   print "leave B"

class C(A):
  def __init__(self):
   print "enter C"
   super(C, self).__init__()
   print "leave C"

class D(A):
  def __init__(self):
   print "enter D"
   super(D, self).__init__()
   print "leave D"
class E(B, C):
  def __init__(self):
   print "enter E"
   super(E, self).__init__()  # change
   print "leave E"

class F(A, B):
  def __init__(self):
   print "enter F"
   super(F, self).__init__()  # change
   print "leave F"

f = F()