
import sqlite3, time
print("START:")

def create_table_uniqueTracks(curs):
    print("Creating uniqueTracks")
    curs.execute("""CREATE TABLE tracks(
            id_wykonania text,
            id_utworu text,
            artysta text,
            tyt_utworu text
            )""")
    print("UniqueTracks created")

#####################################################

def populate_table_uniqueTracks(curs):
    print("Pupulating uniqueTracks")
    with open("unique_tracks.txt" , encoding='ANSI') as f:
        for line in f:
            tablica = line.split('<SEP>')
            curs.execute("INSERT INTO tracks VALUES (?,?,?,?)", tablica)
    print("UniqueTracks populated")

#####################################################

def remove_duplicates_uniqueTracks(curs):
    print("Removing duplicates from uniqueTracks")
    curs.execute("""DELETE FROM tracks
    WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM tracks 
    GROUP BY id_utworu )"""
                )
    print("UniqueTracks duplicates removed")

#####################################################

def create_table_triplets(curs):
    print("Creating triplets")
    curs.execute("""CREATE TABLE triplets(
                    id_usera text,
                    id_utworu text,
                    data text)"""
                )
    print("Triplets created")

#####################################################

def populate_table_triplets(curs):
    print("Populating triplets")
    with open("triplets_sample_20p.txt" , encoding='ANSI') as f:
        for line in f:
            tablica = line.split('<SEP>')
            curs.execute("INSERT INTO triplets VALUES (?,?,?)", tablica)
    print("Triplets populated")

#####################################################

def most_popular_artist(curs):
    print("\nFinding most popular artist...")
    curs.execute("""SELECT DISTINCT count(artysta), tra.artysta 
    FROM triplets tri INNER JOIN tracks tra ON tra.id_utworu = tri.id_utworu
    GROUP BY tra.artysta
    ORDER BY count(artysta) DESC
    LIMIT 1
    """)
    temp = curs.fetchone()
    print("Most popular artist is: ", temp[1],
    "with tracks played:", temp[0], "times.\n")

#####################################################

def most_popular_tracks(curs):
    print("Finding 5 most popular tracks...")
    curs.execute("""SELECT count(tri.id_utworu), tra.artysta, tra.tyt_utworu 
    FROM triplets tri INNER JOIN tracks tra ON tra.id_utworu = tri.id_utworu
    GROUP BY tri.id_utworu
    ORDER BY count(tri.id_utworu) DESC
    LIMIT 5
    """)
    temp = list(curs.fetchmany(5))

    for item in temp:
        tab = [item[0],item[1],item[2]]
        tab[2] = tab[2].replace('\n','')
        print("\nTrack:", item[2])
        print("from:", item[1])
        print("listened:", item[0], "times.")

#####################################################


timee = time.time()
conn = sqlite3.connect('temporary.db')

cursorr = conn.cursor()

create_table_uniqueTracks(cursorr)

populate_table_uniqueTracks(cursorr)

remove_duplicates_uniqueTracks(cursorr)

create_table_triplets(cursorr)

populate_table_triplets(cursorr)

most_popular_artist(cursorr)

most_popular_tracks(cursorr)

conn.commit()
conn.close()
     
print("Time: ", time.time() - timee ," seconds")