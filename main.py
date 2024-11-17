from sqlmodel import  Field, SQLModel, create_engine, Session, select, or_


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpool", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)


        print("\n")
        print("After adding to the session")
        print("Hero 1: ", hero_1)
        print("Hero 2: ", hero_2)
        print("Hero 3: ", hero_3)

        session.commit()

        # This is empty as data has been committed already to the database
        print("\n")
        print("After committing the session")
        print("Hero 1: ", hero_1)
        print("Hero 2: ", hero_2)
        print("Hero 3: ", hero_3)

        # Session is refreshed here inorder to get this information
        print("\n")
        print("After committing the session, show IDs")
        print("Hero 1 ID:", hero_1.id)
        print("Hero 2 ID:", hero_2.id)
        print("Hero 3 ID:", hero_3.id)

        # Session is refreshed here inorder to get this information
        print("\n")
        print("After committing the session, show names")
        print("Hero 1 name:", hero_1.name)
        print("Hero 2 name:", hero_2.name)
        print("Hero 3 name:", hero_3.name)

        # Refresh Objects Explicitly
        session.refresh(hero_1)
        session.refresh(hero_2)
        session.refresh(hero_3)

        # Finally, this will be returning the items since session is refreshed.
        print("\n")
        print("After refreshing the heroes")
        print("Hero 1: ", hero_1)
        print("Hero 2: ", hero_2)
        print("Hero 3: ", hero_3)

    # Print data after closing the session
    print("\n")
    print("After the session closes")
    print("Hero 1: ", hero_1)
    print("Hero 2: ", hero_2)
    print("Hero 3: ", hero_3)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement)
        # for hero in results:   # -> This returns an iterable
        #     print(hero)
        #

        # More compact version
        # heroes = session.exec(select(Hero)).all()

        heroes = results.all()
        print(heroes)

def select_heroes_where():
    with Session(engine) as session:
        statement = select(Hero).where(or_(Hero.age <= 35, Hero.age > 90 ))
        results = session.exec(statement)
        for hero in results:
            print(hero)
        # You could even do
        # statement = select(Hero).where(Hero.name == "Deadpool").where(Hero.age == 48)

def select_heroes_one_row():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpool")
        results = session.exec(statement)
       # hero = results.first()
       #  hero = results.one()
       #  print("Hero:", hero)

        # Compact Version
        hero = session.exec(select(Hero).where(Hero.name == "Deadpool")).one()
        print("Hero:", hero)

def select_heroes_by_id_with_where():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == 1)
        results = session.exec(statement)
        hero = results.first()
        print("Hero:", hero)


def select_heroes_by_id_with_get():
    with Session(engine) as session:
        hero = session.get(Hero, 1)
        print("Hero:", hero)

def select_heroes_with_get_with_no_data():
    with Session(engine) as session:
        hero = session.get(Hero, 9001)
        print("Hero:", hero)


def main():
    # create_db_and_tables()
    # create_heroes()
    select_heroes_one_row()
    print("\n")
    select_heroes_by_id_with_where()
    print("\n")
    select_heroes_by_id_with_get()
    print("\n")
    select_heroes_with_get_with_no_data()

if __name__ == '__main__':
    main()
