# Import libraries required for connecting to mysql
import mysql.connector

# Import libraries required for connecting to PostgreSql
import psycopg2

# Connect to MySQL
connection = mysql.connector.connect(user='root', password='MjQ3Nzgta2hhaXJp',host='127.0.0.1',database='sales')
cursorMy = connection.cursor()

# Connect to PostgreSql
conn = psycopg2.connect(
    host="localhost",
    database="ecommerce",
    user="postgres",
    password="MzA3NS1raGFpcmls")
cursorP = conn.cursor()

# Find out the last rowid from PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the PostgreSql.
def get_last_rowid():
    cursorP.execute('SELECT MAX(rowid) FROM sales_data;')
    row = cursorP.fetchone()
    conn.commit()
    return int(row[0])


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.
def get_latest_records(rowid):
    SQL = "SELECT * FROM sales_data WHERE rowid > %s"
    cursorMy.execute(SQL, [rowid])
    new_recs = cursorMy.fetchall()
    return new_recs

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in PostgreSql.
def insert_records(records):
    for record in records:
        SQL="INSERT INTO sales_data(rowid,product_id,customer_id, quantity) VALUES(%s,%s,%s,%s)" 
        cursorP.execute(SQL,record);
        conn.commit()

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()

# disconnect from PostgreSql data warehouse 
conn.close()
# End of program