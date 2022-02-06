#Practice with Python Data Structures

class PartyAnimal: #A template
  x = 0

  def part(self):
      self.x = self.x + 1
      print("One",self.x)

an = PartyAnimal() #class is a template for an
an.part()
an.part() #only takes self so (an), can't give it arguements
an.part()
print(type(PartyAnimal))
print(dir(PartyAnimal))

