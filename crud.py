from db import get_db_connection, close_db_connection

# ✅ Create a new criminal
def create_criminal(name, age, crime_type):
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}
    
    cursor = connection.cursor()
    query = "INSERT INTO criminals (name, age, crime_type) VALUES (%s, %s, %s)"
    values = (name, age, crime_type)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Criminal added successfully", "criminal_id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Get all criminals
def get_criminals():
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM criminals"
    
    try:
        cursor.execute(query)
        criminals = cursor.fetchall()
        return criminals
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Create a new case
def create_case(case_title, description, date_reported, criminal_id):
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor()
    query = "INSERT INTO cases (case_title, description, date_reported, criminal_id) VALUES (%s, %s, %s, %s)"
    values = (case_title, description, date_reported, criminal_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Case added successfully", "case_id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Get all cases
def get_cases():
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM cases"

    try:
        cursor.execute(query)
        cases = cursor.fetchall()
        return cases
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Get cases by criminal ID
def get_cases_by_criminal(criminal_id):
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM cases WHERE criminal_id = %s"
    
    try:
        cursor.execute(query, (criminal_id,))
        cases = cursor.fetchall()
        return cases
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Delete a criminal by ID
def delete_criminal(criminal_id):
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor()
    query = "DELETE FROM criminals WHERE id = %s"

    try:
        cursor.execute(query, (criminal_id,))
        connection.commit()
        return {"message": "Criminal deleted successfully"} if cursor.rowcount > 0 else {"error": "Criminal not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ Delete a case by ID
def delete_case(case_id):
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    cursor = connection.cursor()
    query = "DELETE FROM cases WHERE id = %s"

    try:
        cursor.execute(query, (case_id,))
        connection.commit()
        return {"message": "Case deleted successfully"} if cursor.rowcount > 0 else {"error": "Case not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        close_db_connection(connection)
