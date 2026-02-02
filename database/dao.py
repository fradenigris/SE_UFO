from database.DB_connect import DBConnect
from model.state import State

class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YEAR(s_datetime) AS year
                    FROM sighting
                    WHERE YEAR(s_datetime) >= 1910
                    AND YEAR(s_datetime) <= 2014 """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shape_specific_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape
                    FROM sighting
                    WHERE YEAR(s_datetime) = %s
                    AND shape IS NOT NULL """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_count_specific_state(year, shape, state):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT count(state) conteggio
                    FROM sighting
                    WHERE YEAR(s_datetime) = %s
                    AND shape = %s
                    AND UPPER(state) = %s """

        cursor.execute(query, (year, shape, state))

        for row in cursor:
            number = row['conteggio']
            result.append(number)

        cursor.close()
        conn.close()
        return result[0]

    @staticmethod
    def get_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, name, lat, lng, area
                    FROM state """

        cursor.execute(query)

        for row in cursor:
            result.append(State(
                id=row['id'],
                name=row['name'],
                lat=row['lat'],
                lng=row['lng'],
                area=row['area']
            ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_neighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state1, state2
                    FROM neighbor """

        cursor.execute(query)

        for row in cursor:
            tupla = (row['state1'], row['state2'])
            result.append(tupla)

        cursor.close()
        conn.close()
        return result