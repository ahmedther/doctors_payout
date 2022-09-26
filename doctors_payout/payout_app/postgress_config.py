import psycopg2


from datetime import datetime

db_name = "doctors_payout_database"
username = "postgres"
password = "ahmed"
host = "172.20.100.81"
port = 5432


class PostgressDB:
    def __init__(self):
        # Connect to your postgres DB
        self.connection = psycopg2.connect(
            host=host, dbname=db_name, user=username, password=password, port=port
        )
        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()

    def connection_close(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def applicable_doctors(self):
        get_report_query = f"""
        
        SELECT * FROM payout_app_doctorprofile
        ORDER BY id ASC 

        """

        self.cursor.execute(get_report_query)
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        self.connection_close()
        return data, column_name

    def transplant_doctors(self, department):
        get_transplant_query = f"""
        SELECT doctors_name,doctors_share, doctors_department
        FROM public.payout_app_transplant
        INNER JOIN payout_app_doctorprofile on payout_app_transplant.doctors_name_id = payout_app_doctorprofile.id
		where doctors_department = '{department}'
        """
        self.cursor.execute(get_transplant_query)
        data = self.cursor.fetchall()
        column_name = [i[0] for i in self.cursor.description]
        self.connection_close()
        return data, column_name


if __name__ == "__main__":
    from_date = "2022-07-19"
    db = PostgressDB()
    a = db.get_report(from_date, from_date)
