#Practice with Python Data Structures

class PartyAnimal: #A template
  x = 0
  name = ""
  def __init__(self,z): #constructor, self passes in instance of this particular one
      self.name = z
      print(self.name, "constructed")

  def part(self):
    self.x = self.x + 1
    print(self.name, "party count", self.x)

class FootballFan(PartyAnimal): #Class gets passed into FootballFan (Inheritance) Extension
    points = 0
    def touchdown(self):
        self.points = self.points + 7
        self.part()
        print(self.name,"points",self.points)

x = PartyAnimal("Bob") #a object x is created using template
x.part()
print("\r")
y = FootballFan("Brad") #inherits all the properties from PartyAnimal template + FootballFan due to class being passed in
y.part()
y.touchdown()