# Gluer

*Dependency Injection for Python*

### Installation

Gluer uses [type annotations](https://www.python.org/dev/peps/pep-0484/), so python 3.6+ is required

	python3 -m pip install --user gluer


### Usage


Let's follow a [wonderful explanation](https://stackoverflow.com/a/1638961/4339338) of DI:


```python
from abc import ABC, abstractmethod
from gluer import Gluer

class Drink(ABC): # this doesn't *have* to be abstract
	@abstractmethod
	def sip(self):
		pass


class Child:
	def __init__(self, drink: Drink):
		self.drink = drink

	def take_a_sip(self):
		self.drink.sip()
		print("ahhh")


class Juice(Drink):
	def sip(self):
		print("*gulp*")


class Coke(Drink):
	def sip(self):
		print("*fizzle*")



if __name__ == "__main__":
	gluer = Gluer()
	mom_watches = True

	gluer.register(Child)
	gluer.register(Juice if mom_watches else Coke).As(Drink)

	container = gluer.build()

	kid = container.resolve(Child)
	kid.take_a_sip() # *gulp* ahhh
```

