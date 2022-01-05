import sqlite3

#connection to database
conn = sqlite3.connect('database.db')



#executing sql file
with open('schema.sql') as f:
    conn.executescript(f.read())



#cursor reads the query and connect to database
cur = conn.cursor()

cur.execute("INSERT INTO violators (last_name, first_name, middle_name, house_number, street, barangay, contact, violation, penalty, total_penalty, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", ("Malla", "Lorenzo", "Borja", "100", "Pulang Lupa", "San Francisco", "9653926888", "No Face Shield", "300", "1", "Pending"))



cur.execute("INSERT INTO violations (violation, name) VALUES (?,?)", ("No Face Mask", "No Face Mask"))
cur.execute("INSERT INTO violations (violation, name) VALUES (?,?)", ("No Face Shield", "No Face Mask"))
cur.execute("INSERT INTO violations (violation, name) VALUES (?,?)", ("No Social Distancing", "No Face Mask"))
cur.execute("INSERT INTO violations (violation, name) VALUES (?,?)", ("Curfew", "No Face Mask"))

cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Banca Banca", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Daniw", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Masapang", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Nanhaya", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Pagalangan", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("San Benito", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("San Felix", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("San Francisco", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("San Roque", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Accounting", "No Face Mask"))
cur.execute("INSERT INTO barangays (barangay, name) VALUES (?,?)", ("Municipal", "No Face Mask"))

cur.execute("INSERT INTO stat (status, penalty) VALUES (?,?)", ("Pending", "300"))
cur.execute("INSERT INTO stat (status, penalty) VALUES (?,?)", ("Done", "Community Service"))

cur.execute("INSERT INTO purok (purok, puroks) VALUES (?,?)", ("Purok I", "Purok I"))
cur.execute("INSERT INTO purok (purok, puroks) VALUES (?,?)", ("Purok II", "Purok II"))
cur.execute("INSERT INTO purok (purok, puroks) VALUES (?,?)", ("Purok III", "Purok III"))

cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("lorenzo", "lorenzomalla1@gmail.com", "123123", "asdasd", "Banca Banca"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("jessica", "lorenzomalla2@gmail.com", "123123", "asdasd", "Daniw"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("jeff", "lorenzomalla3@gmail.com", "123123", "asdasd", "Masapang"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("edd", "lorenzomalla4@gmail.com", "123123", "asdasd", "Nanhaya"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("mark", "lorenzomalla5@gmail.com", "123123", "asdasd", "Pagalangan"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("dessa", "lorenzomalla6@gmail.com", "123123", "asdasd", "San Benito"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("jom", "lorenzomalla7@gmail.com", "123123", "asdasd", "San Felix"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("walter", "lorenzomalla8@gmail.com", "123123", "asdasd", "San Francisco"))
cur.execute("INSERT INTO user (username, mail, password, hashCode, category) VALUES (?,?,?,?,?)", ("kae", "lorenzomalla9@gmail.com", "123123", "asdasd", "San Roque"))

conn.commit()
conn.close()
