from dataclasses import field
from marshmallow_dataclass import dataclass  # Importing from marshmallow_dataclass instead of dataclasses
import marshmallow.validate
from typing import List, Optional


@dataclass
class Building:
  # The field metadata is used to instantiate the marshmallow field
  height: float = field(metadata={'validate': marshmallow.validate.Range(min=0)})
  name: str = field(default="anonymous")


@dataclass
class City:
  name: Optional[str]
  buildings: List[Building] = field(default_factory=lambda: [])


# City.Schema contains a marshmallow schema class
city = City.Schema().load({
    "name": "Paris",
    "buildings": [
        {"name": "Eiffel Tower", "height": 324}
    ]
})

# Serializing city as a json string
city_json = City.Schema().dumps(city)

print(city_json)