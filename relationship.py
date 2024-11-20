from sqlmodel import Field, SQLModel, create_engine, Relationship, Session, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquaters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id", ondelete="SET NULL")
    team: Team | None = Relationship(back_populates="heroes")


sqlite_file_name = "database1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create Instances with Relationship Attributes

def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquaters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquaters="Sister Marget's Bar")

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_z_force)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)

        session.commit()
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created Hero:", hero_deadpond)
        print("Created Hero:", hero_rusty_man)
        print("Created Hero:", hero_spider_boy)

# Create a Team with Heroes
def create_team_with_heroes():
    with Session(engine) as session:

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")

        team_wakaland = Team(name="Wakaland", headquaters="Wakaland Capital City", heroes=[hero_black_lion, hero_sure_e])

        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("Team Wakaland:", team_wakaland)


# Include Relationship Objects in the Many Side

def create_heroes_in_the_many_side():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        resluts = session.exec(statement)
        team_preventers = resluts.one()

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)

        session.add(team_preventers)
        session.commit()

        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)

        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)


# Read Relationships
def select_heroes_with_relationship():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()

        # Get Relationship Team -> New Way
        print("Spider-Boy's team:", hero_spider_boy.team)


# GEt a list of Relationship Objects
def select_heroes_list_relationship():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        team_preveneters = results.one()

        print("Preventers heroes", team_preveneters.heroes)


# Remove Relationship
def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        result = session.exec(statement)
        hero_spider_boy = result.one()

        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_spider_boy)
        print("Spider-Boy without team:", hero_spider_boy)

# Cascade Delete Team
def delete_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Wakaland")
        team = session.exec(statement).one()
        session.delete(team)
        session.commit()
        print("Deleted Team:", team)

def main():
    # create_db_and_tables()
    # create_heroes()
    # create_team_with_heroes()
    # create_heroes_in_the_many_side()
    # select_heroes_with_relationship()
    # select_heroes_list_relationship()
    # update_heroes()
    delete_team()


if __name__ == '__main__':
    main()