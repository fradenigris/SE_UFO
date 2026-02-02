from dataclasses import dataclass

@dataclass
class State:
    id : str
    name : str
    lat : float
    lng : float
    area : float

    def __str__(self):
        return f"{self.id}, name: {self.name}, neighbors: {self.neighbors}"

    def __repr__(self):
        return f"{self.id}, name: {self.name}, neighbors: {self.neighbors}"

    def __hash__(self):
        return hash(self.id)