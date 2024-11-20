from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquaters: str

    heroes: list["Hero"] = Relationship()


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Team | None = Relationship()


sqlite_file_name = "database3.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquaters="Sharp-Tower")
        team_z_force = Team(name="Z-Force", headquaters="Sister Margaret's Bar")

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

        print("\n")
        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("\n")
        print("Updated hero:", hero_spider_boy)

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(name="Wakaland", headquaters="Wakaland Capital City", heroes=[hero_black_lion, hero_sure_e])
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print("\n")
        print("Team Wakaland:", team_wakaland)

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
        print("\n")
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)

# Read Data Objects
def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        preventers_team = session.exec(select(Team).where(Team.name == "Preventers")).one()

        # Print the Data
        print("Hero Spider-Boy:", hero_spider_boy)
        print("Preventers Team:", preventers_team)
        print("Preventers Team Heroes:", preventers_team.heroes)


def update_heroes_before_commiting():
    with Session(engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        preventers_team = session.exec(select(Team).where(Team.name == "Preventers")).one()

        hero_spider_boy.team = None

        print("\n")
        print("Spider-Boy without team:", hero_spider_boy)
        print("\n")
        print("Preventers Team Heroes again:", preventers_team.heroes)


def update_heroes_after_commiting():
    with Session(engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        preventers_team = session.exec(select(Team).where(Team.name == "Preventers")).one()

        hero_spider_boy.team = None

        session.add(hero_spider_boy)
        session.commit()
        print("After commiting")

        session.refresh(hero_spider_boy)
        print("Spider-Boy after team:", hero_spider_boy)
        print("\n")
        print("Preventers Team Heroes after commit:", preventers_team.heroes)


def main():
    # create_db_and_tables()
    # create_heroes()
    # update_heroes()
    # update_heroes_before_commiting()
     update_heroes_after_commiting()


if __name__ == '__main__':
    main()