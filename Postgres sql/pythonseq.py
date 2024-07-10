import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="pg.pg4e.com",  # replace with your database host
    database="pg4e_b5db3af9e1",  # replace with your database name
    user="pg4e_b5db3af9e1",  # replace with your database username
    password="pg4e_p_acc9970b85588f9"  # replace with your database password
)

# Create a cursor object
cur = conn.cursor()

# Create the table
cur.execute("""
    CREATE TABLE IF NOT EXISTS pythonseq (
        iter INTEGER,
        val INTEGER
    );
""")

# Initialize the pseudorandom number sequence
value = 647782

# Generate and insert 300 pseudorandom numbers
for i in range(300):
    cur.execute("INSERT INTO pythonseq (iter, val) VALUES (%s, %s)", (i + 1, value))
    value = int((value * 22) / 7) % 1000000

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data inserted successfully")
