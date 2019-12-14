import requests
import json
import sqlite3
from os.path import dirname, abspath


r = requests.get('https://cashcog.xcnt.io/stream', stream=True)
count = 0
max_count = 5
validated_data = dict() # we use this later to load the data to a db, say sqlite.

table_mapping = {
    "employee": "backendapp_employee",
    "expense": "backendapp_expense"
}

for line in r.iter_lines():
    # filter out keep-alive new lines
    if line:
        decoded_line = line.decode('utf-8')
        print("got stream data: {}".format(decoded_line))
        validated_data[count] = json.loads(decoded_line)
        count += 1
        if count == max_count: break

dbfile = "{}/db.sqlite3".format(dirname(dirname(dirname(abspath(__file__)))))
print(dbfile)

conn = sqlite3.connect(dbfile)
c = conn.cursor()

employee_table = table_mapping.get('employee')
espense_table = table_mapping.get('expense')

# load the employee details first as Expense table uses this as a foreign key.
for i, data in validated_data.items():
    data_item = 'employee'
    if data_item in data:
        employee_uuid = data[data_item]['uuid'].replace("-", "")
        first_name = data[data_item]['first_name']
        last_name = data[data_item]['last_name']
        try:
            employee_exists = False
            employee_id = c.execute('SELECT id FROM {} WHERE uuid="{}"'.
                                     format(table_mapping.get(data_item), employee_uuid))
            employee_id = employee_id.fetchone()
            if employee_id:
                employee_exists = True
                employee_id = 1

            if not employee_exists:
                total = c.execute('SELECT count(*) FROM {}'.format(table_mapping.get(data_item)))
                total = total.fetchone() or [0]
                next_id = total[0] + 1
                c.execute(
                'INSERT INTO {}(id, uuid, first_name, last_name) VALUES(?, ?, ?, ?)'.
                    format(table_mapping.get(data_item)),
                    [next_id, employee_uuid, first_name, last_name])
                employee_id = next_id
        except Exception as e:
            print("failed to insert into Employee table: {}".format(data, data_item))
            print(e.args[0])

        data_item = 'expense'

        uuid = data.get("uuid").replace("-", "")
        description = data.get("description")
        created_at = data.get("created_at")
        amount = data.get("amount")
        currency = data.get("currency")
        expense_approved = False

        c.execute(
            'INSERT INTO {}(uuid, description, created_at, amount, currency, employee_id, expense_approved) '
            'VALUES(?, ?, ?, ?, ?, ?, ?)'. format(table_mapping.get(data_item)),
            [uuid, description, created_at, amount, currency, employee_id, expense_approved])

conn.commit()
conn.close()