from flask.cli import with_appcontext
import click
import csv
from os import path
from datetime import datetime, timedelta

from src.models import Category, Center, User, Role, DynamicTable, Subscription
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
            new_category.create()

    click.echo("Adding test user")

    new_role = Role(name="User", is_admin=False)
    new_role.create()

    new_role = Role(name="Admin", is_admin=True)
    new_role.create()

    new_user = User(email='varsimashvili.official@gmail.com',
                    password='TESTtest123',
                    verified=True,
                    role=new_role)
    new_user.create()

    click.echo("Test user added successfully")
    click.echo("First tables added")

    click.echo("Adding empty dymanic data")
            # Create a new Station instance for each row
    city_ids = [2,3,4,5,6,7,8,9,10,15]
    transmition_ids = [3,4]

    for i in city_ids:
        for j in transmition_ids:
            new_dynamic_data = DynamicTable(official_center_id=i,official_category_id=j,availability={})
            new_dynamic_data.create()
    click.echo("Added empty dymanic data")


@click.command("insert_db")
@with_appcontext
def insert_db():
    # testing
    subscriptions = Subscription.query.filter_by(id=1).first()
    subscriptions.email_sent_at = datetime.now() - timedelta(days=14)
    subscriptions.save()
    # for i in subscriptions:
    #     i.status = True
    #     i.save()


    
    pass
