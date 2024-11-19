from sqlmodel import Field, SQLModel, create_engine, select, Session, Relationship

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

    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Team | None = Relationship(back_populates="heroes")


sqlite_file_name = "database2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create Rows for Teams with SQLModel

def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquaters="Sharp Tower")
        team_z_forec = Team(name="Z-Force", headquaters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_forec)
        session.commit()

        # Create Rows for Heroes in code
        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team_id=team_z_forec.id)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team_id=team_preventers.id)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        # Refresh and Print Heroes
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

# Read connected data
def select_heroes_related_data():
    with Session(engine) as session:
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)

# Join tables in SQLModel
def select_heroes_related_data_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)


# Left outer join
def select_heroes_left_outer_join():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)


def select_heroes_only_but_join_with_teams():
    """Here we are filtering with .where() to get only the heroes that belong to the preventers team.
       But we are still only requesting the data from heroes, not their teams.

       You can include the Team information as well by including the team in:
        select(Hero, Team).join(Team).where(Team.name == "Preventers")
    """
    with Session(engine) as session:
        statement = select(Hero).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        for hero in results:
            print("Preventer Hero:", hero)

# Update Data Connections
def update_hero_data_connections():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_spider_boy = results.one()

        statement = select(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        team_preventers = results.one()

        hero_spider_boy.team_id = team_preventers.id

        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

# Break a Connection

def remove_data_connections():
    """We don't really have to delete anything to break a connection. We can just assign `None` to
       the foreign key, in this case , to the `team_id`.

       Let's say Spider-Boy is tired of lack of friendly neighbours and wants to get out of the Preventers.
       We can just simply set the `team_id` to `None` and now it doesn't have a connection with the team.
    """
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_spider_boy = results.one()

        hero_spider_boy.team_id = None

        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("No Longer a Preventer:", hero_spider_boy)

def main():
    #create_db_and_tables()
    #create_heroes()
    # select_heroes_related_data()
    # print("\n")
    # select_heroes_related_data_join()
    # print("\n")
    # select_heroes_left_outer_join()
    # print("\n")
    # select_heroes_only_but_join_with_teams()
    # print("\n")
    # update_hero_data_connections()
    # print("\n")
    remove_data_connections()

if __name__ == "__main__":
    main()
