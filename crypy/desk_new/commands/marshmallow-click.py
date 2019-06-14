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

import click



@click.group("Cities")
@click.pass_context
def cities(ctx):
    ctx.obj={city.name: city}


@cities.command()
@click.pass_obj
def browse(obj):
    """browse all cities"""
    for n, c in obj.items():
        click.echo(n + ":")
        click.echo(c)

@cities.command()
@click.argument("name")
@click.pass_obj
def read(obj, name):
    click.echo(obj.get(name))


def edit(name):
    #TODO : interactive repl ?? all in cmd line ???
    pass


@cities.command()
@click.argument("name")
@click.argument("city")
@click.pass_obj
def add(obj, name, city):
    obj[name] = city


@cities.command()
@click.argument("name")
@click.pass_obj
def delete(obj, name):
    click.echo(obj.pop(name))



if __name__ == '__main__':
    cities()



