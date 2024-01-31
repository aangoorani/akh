from datetime import datetime
import mysql.connector
import json
import threading
import time

with open('config.json') as fp:
    config = json.load(fp)

# Replace these with your actual database details
host, port = config["db_address_1"].split(':')
database = config["db_name"]
password = config["db_password"]
user = config["db_user"]
port = int(port)

# Establish a connection
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    # database=database
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

db_lock = threading.Lock()  # Used for synchronizing access to the DB


def insert_table(address):
    """Insert data into the Monitoring_System table."""

    with db_lock:
        try:
            insert_query = """
            INSERT INTO Monitoring_System (address, success, failiure, created_at)
            VALUES (%s, %s, %s, %s)
            """
            data = (address, 0, 0, time.time())
            cursor.execute(insert_query, data)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise Exception("Error inserting into database: %s" % e)



def human_readable_timestamp(ts):
    """Convert a UNIX timestamp to a more human-friendly format."""
    try:
        human_readable_date = datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")   
    except Exception as e:
        # print(str(e))
        human_readable_date = 'NULL'
    return human_readable_date        

    

def get_row(id):
    with db_lock:
        select_query = "SELECT * FROM Monitoring_System WHERE id=%s"
        cursor.execute(select_query, (id,))
        row = cursor.fetchone()

        if row:
            # Convert the row to a dictionary
            row_dict = {
                "id": row[0],
                "address": row[1],
                "success": row[2],
                "failiure": row[3],
                "last_failiure": human_readable_timestamp(row[4]),  # Convert timestamp to string
                "created_at": human_readable_timestamp(row[5])  # Convert timestamp to string
            }

            return row_dict
        else:
            return None
    

def get_all_rows():
    with db_lock:
        select_query = "SELECT * FROM Monitoring_System ORDER BY created_at DESC"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Convert each row to a dictionary and append it to the list of results
        result = []
        for row in rows:
            if row:
            # Convert the row to a dictionary
                row_dict = {
                    "id": row[0],
                    "address": row[1],
                    "success": row[2],
                    "failiure": row[3],
                    "last_failiure": human_readable_timestamp(row[4]),  # Convert timestamp to string
                    "created_at": human_readable_timestamp(row[5])  # Convert timestamp to string
                }

                result.append(row_dict)
        return result


def update_by_address(address, inc_dec):
    """Update the monitoring status by address."""
    with db_lock:
        if inc_dec >= 0:
            update_query = """UPDATE Monitoring_System
                                SET success = success + 1
                                WHERE address = %s"""
            data = (address,)
            
        else:
            update_query = """UPDATE Monitoring_System
                                SET failiure = failiure + 1,
                                    last_failiure = %s
                                WHERE address = %s"""
            data = (time.time(), address)
            

        cursor.execute(update_query, data)
        conn.commit()

        return cursor.lastrowid
       

def close_connection():
    """Close the database connection."""
    with db_lock:
        cursor.close()
        conn.close()


def create_table():
    """Create a table in the MySQL database"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Monitoring_System (
        id INT AUTO_INCREMENT PRIMARY KEY,
        address VARCHAR(255) NOT NULL,
        success INT,
        failiure INT,
        last_failiure VARCHAR(255),
        created_at VARCHAR(255) NOT NULL,
        UNIQUE(address)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()


def create_database():
    """Check if the required database exists and create it if not"""
    try:
    # Check if the database exists
        cursor.execute(f"USE {database}")
        print(f"Database '{database}' already exists.")

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            # The database does not exist, create it
            create_db_query = f"CREATE DATABASE {database}"
            cursor.execute(create_db_query)
            print(f"Database '{database}' created successfully.")
            cursor.execute(f"USE {database}")
            
        else:
            # Other error, print the error message
            print("Error:", err)


def setup_database():
    create_database()
    create_table()
