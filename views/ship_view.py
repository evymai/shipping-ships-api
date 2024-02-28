import sqlite3
import json


def add_ship(ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Ship (name, hauler_id)
            VALUES (?, ?)
            """,
            (ship_data["name"], ship_data["hauler_id"]),
        )

        conn.commit()

        return db_cursor.lastrowid


def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data["name"], ship_data["hauler_id"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Ship WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url_dictionary):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "_expand" in url_dictionary["query_params"]:
            db_cursor.execute(
                """
            SELECT 
                s.id,
                s.name,
                s.hauler_id,
                h.id as haulerId,
                h.name as haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            """
            )
        else:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            """
            )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        ships = []
        for row in query_results:
            ship = {
                "id": row["id"],
                "name": row["name"],
                "hauler_id": row["hauler_id"],
            }
            if "_expand" in url_dictionary["query_params"]:
                hauler = {
                    "id": row["haulerId"],
                    "name": row["haulerName"],
                    "dock_id": row["dock_id"],
                }
                ship["hauler"] = hauler
            ships.append(ship)
        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships


def retrieve_ship(pk, url_dictionary):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if "_expand" in url_dictionary["query_params"]:
            db_cursor.execute(
                """
            SELECT 
                s.id,
                s.name,
                s.hauler_id,
                h.id as haulerId,
                h.name as haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            WHERE s.id = ?
            """,
                (pk,),
            )
        else:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            WHERE s.id = ?
            """,
                (pk,),
            )
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        ship_info = {
            "id": query_results["id"],
            "name": query_results["name"],
            "hauler_id": query_results["hauler_id"],
        }
        if "_expand" in url_dictionary["query_params"]:
            ship_info["hauler"] = {
                "id": query_results["haulerId"],
                "name": query_results["haulerName"],
                "dock_id": query_results["dock_id"],
            }
        serialized_ship = json.dumps(ship_info)

    return serialized_ship
