import csv
from datetime import datetime
import MySQLdb

def import_csv_to_mysql(csv_file, db_host, db_user, db_password, db_name, table_name):
    
    try:
        conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            region         VARCHAR(50) NOT NULL 
            ,country        VARCHAR(50) NOT NULL
            ,item_type      VARCHAR(20) NOT NULL
            ,sales_channel  VARCHAR(10) NOT NULL
            ,order_priority VARCHAR(5) NOT NULL
            ,order_date     DATE  NOT NULL
            ,order_id       INTEGER  NOT NULL PRIMARY KEY
            ,ship_date      DATE  NOT NULL
            ,units_sold     INTEGER  NOT NULL
            ,unit_price     NUMERIC(10,2) NOT NULL
            ,unit_cost      NUMERIC(10,2) NOT NULL
            ,total_revenue  NUMERIC(10,2) NOT NULL
            ,total_cost     NUMERIC(10,2) NOT NULL
            ,total_profit   NUMERIC(10,2) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        
        row = 0
        with open(csv_file, 'r') as file:
            reader=csv.reader(file)
            next(reader)
            for row in reader:
                region,country,item_type,sales_channel,order_priority,order_date,order_id,ship_date,units_sold, unit_price,unit_cost,total_revenue,total_cost,total_profit= row
                order_date =datetime.strptime(order_date, "%m/%d/%Y").strftime("%Y-%m-%d")
                ship_date = datetime.strptime(ship_date, "%m/%d/%Y").strftime("%Y-%m-%d")
                insert_query = f"""
                INSERT INTO {table_name} (region,country,item_type,sales_channel,order_priority,
                order_date,order_id,ship_date,units_sold,unit_price,unit_cost,total_revenue,total_cost,total_profit)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(insert_query,[region,country,item_type,sales_channel,order_priority,order_date,order_id, ship_date,units_sold,unit_price,
                unit_cost,total_revenue,total_cost,total_profit])

        print("Dataset imported to MySQL database...")
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print("Error: ",str(e))

if __name__ == "__main__":
    # Replace the following variables with your database credentials and CSV file path
    csv_file_path = '10000 Sales Records.csv'
    db_host = '127.0.0.1'
    db_user = 'root'
    db_password = ''
    db_name = 'sales_db'
    table_name = 'sales'

    import_csv_to_mysql(csv_file_path, db_host, db_user, db_password, db_name, table_name)
