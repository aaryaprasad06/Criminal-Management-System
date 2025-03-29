import mysql.connector
from mysql.connector import Error

# ✅ Function to establish a database connection
def get_db_connection():
    """Establish and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",      # Change this if necessary
            user="root",           # Your MySQL username
            password="14112417",   # Your MySQL password
            database="criminal_management"  # Your database name
        )
        if connection.is_connected():
            print("✅ Database connected successfully!")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

# ✅ Function to close the database connection
def close_db_connection(connection):
    """Close the database connection if it's open."""
    if connection and connection.is_connected():
        connection.close()
        print("✅ Database connection closed.")

# ✅ Test the database connection when this script runs directly
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        close_db_connection(conn)
