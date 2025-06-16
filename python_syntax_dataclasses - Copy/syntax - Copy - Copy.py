from typing import ClassVar
from dataclasses import dataclass

@dataclass
class Pakistan:
    national_language: ClassVar[str] = "Urdu"
    name: str
    age: int
    weigth: float
   

    def persons_name(self):
        return f"My name is {self.name}"

    def persons_age(self):
        return self.age

    @staticmethod
    def country_language():
        return Pakistan.national_language  # Urdu is the national language

# Create an instance
person = Pakistan(name="Sidra", age=20, weigth=50.5)

# Print attributes
print(person.name)          # Sidra
print(person.age)           # 20
print(person.weigth)        # 50.5

# Call static method
print(Pakistan.country_language())  # Urdu
