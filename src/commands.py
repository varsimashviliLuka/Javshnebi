from flask.cli import with_appcontext
import click
import csv
from os import path

from src.models import Category, Center
from src.extensions import db
from src import Config

@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")

@click.command("populate_db")
@with_appcontext
def populate_db():
    centers_csv_path = path.join(Config.BASE_DIR, "centers_csv_path.csv")
    categories_csv_path = path.join(Config.BASE_DIR, "categories_csv_path.csv")

    click.echo("Adding centres")
    with open(centers_csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Create a new Station instance for each row
            new_center = Center(
                official_center_id=row['official_center_id'],
                name_georgian=row['name_georgian'],
                name_english=row['name_english']

            )
            new_center.create()

    click.echo("Centres added successfully")

    click.echo("Adding categories")
    with open(categories_csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Create a new Station instance for each row
            new_category = Category(
                official_category_id=row['official_category_id'],
                name_georgian=row['name_georgian'],
                name_english=row['name_english']

            )
            new_center.create()

    click.echo("Categories added successfully")
    click.echo("First tables added")


@click.command("insert_db")
@with_appcontext
def insert_db():
    # ყველა სადგურის სტატუსს ცვლის True-თი
    # stations = Stations.query.all()
    # for i in stations:
    #     i.status = True
    #     i.save()

    
    pass
