#!/usr/local/Python-3.7/bin/python3
import pymysql
import sys
import cgi
import mysql.connector

import cgitb
cgitb.enable()

# print content-type
print("Content-type: text/html\n")

print("""
<html>
<title>Enter New Order</title>
<header>Enter New Order</header>
<body>
""")


print('''
<form action="https://bioed.bu.edu/cgi-bin/students_20/jiliu/jia_add_order.py" method="POST">
product: <select name="product">
 <option value="Book">Book</option>
 <option value="Food">Food</option>
 <option value="Beverage">Beverage</option>
 <option value="Shirt">Shirt</option>
 <option value="Hat">Hat</option>
 <option value="Slippers">Slippers</option>
 </select><br />
 <p>
quantity: <input type="number" name="quantity" /><br />
<p>
name: <input type="text" name="name" /><br />
<p>
<input type="submit" value="go" />
</form>
''')

# get the form
form = cgi.FieldStorage()
product = form.getvalue("product")
#print(product)
quantity = form.getvalue("quantity")
if quantity is not None:
    quantity=int(quantity)
#print('type(quantity):', type(quantity))
name = form.getvalue("name")

if product:
    connection = mysql.connector.connect(host="bioed.bu.edu",user='jiliu', password='jiliu', database='jiliu', port='4253')
    cursor = connection.cursor()

    query0 = """SELECT Product.stock FROM Product WHERE Product.name REGEXP '%s';""" %product
    cursor.execute(query0)
    nowsto = cursor.fetchall()
    nowsto=int(nowsto[0][0])

    if nowsto >= quantity:


        query1 = """SELECT Product.id FROM Product WHERE Product.name REGEXP '%s';""" %product
        #print(query1)
        cursor.execute(query1)
        prid = cursor.fetchall()
        #print('prid:', prid)
        prid=int(prid[0][0])
        #print('now_prid:', prid)
        #print('type(prid):', type(prid))


        query3 = '''INSERT INTO Orders (person_name, product_id,quantity) VALUES ('%s', %i, %i);'''% (name, prid, quantity)
        #print(query3)
        cursor.execute(query3)
        connection.commit()
        
        query4= '''UPDATE Product SET stock = stock - %i WHERE Product.name = '%s';''' %(quantity, product)
        cursor.execute(query4)
        connection.commit()
        
        print("<p><font color=green><b>Success:</b> Order successfuly entered.</font></p>")
        
    else:
        print("<p><font color=red><b>Error:</b> Not enough product in stock.</font></p>")
        
    cursor.close()    
    connection.close()
	


#end the html code
print("""
</body>
</html>
""") 
