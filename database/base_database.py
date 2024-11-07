from peewee import *

conn = SqliteDatabase("database.sqlite")
cursor = conn.cursor()


class BaseModel(Model):
    class Meta:
        database = conn


class Artist(BaseModel):
    artist_id = AutoField(column_name="ArtistId")
    name = TextField(column_name="Name", null=True)

    class Meta:
        table_name = "Artist"


if __name__ == "__main__":
    Artist
    artist = Artist.get(Artist.artist_id == 1)
    print("artist:", artist.artist_id, artist.name)
    conn.close()