import psycopg2
import requests
import json

# Database connection settings (replace with your actual credentials)
conn = psycopg2.connect(
    host="pg.pg4e.com",  # replace with your database host
    database="pg4e_b5db3af9e1",  # replace with your database name
    user="pg4e_b5db3af9e1",  # replace with your database username
    password="pg4e_p_acc9970b85588f9"  # replace with your database password
)

# Create a cursor object
cur = conn.cursor()

# Create the pokeapi table
cur.execute("""
    CREATE TABLE IF NOT EXISTS pokeapi (
        id INTEGER PRIMARY KEY,
        body JSONB
    );
""")
conn.commit()

# Loop through the first 100 Pokémon
for i in range(1, 101):
    url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        
        # Insert data into the table
        cur.execute("INSERT INTO pokeapi (id, body) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", (i, json.dumps(data)))
        conn.commit()
        print(f"Inserted Pokémon ID {i}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve Pokémon ID {i}: {e}")

# Close the cursor and connection
cur.close()
conn.close()

print("Data insertion complete")