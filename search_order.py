#!/usr/local/Python-3.7/bin/python3
import pymysql
import sys
import cgi
import mysql.connector

import cgitb
import datetime

cgitb.enable()

print("Content-type: text/html\n")

print("<html><head>")
print("<title>Search_Orders</title>")

print('''<style>
body {margin:30;padding:30}
#miRNA {
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 50%;
}

#miRNA td, #miRNA th {
  border: 1px solid #ddd;
  padding: 8px;
}

#miRNA tr:nth-child(even){background-color: #f2f2f2;}

#miRNA tr:hover {background-color: #ddd;}

#miRNA th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}
</style>
</head>''')
    
print('<body>')
print("<h1>Search order</h1>")

print('''
<form action="https://bioed.bu.edu/cgi-bin/students_20/jiliu/jia_ordersearch.py" method="POST">

Order ID: <input type="text" name="orderid" /><br />
<p>

product: <select name="product">
 <option value="Unknow">Unknow</option>
 <option value="Book">Book</option>
 <option value="Food">Food</option>
 <option value="Beverage">Beverage</option>
 <option value="Shirt">Shirt</option>
 <option value="Hat">Hat</option>
 <option value="Slippers">Slippers</option>
 </select><br />
 <p>
 
Person name: <input type="text" name="name" /><br />
<p>

Date from: <input type="date" name="datestart" /><br />
To: <input type="date" name="dateend" /><br />
<p>

<input type="submit" value="go" />

</form>
''')


# get the form
form = cgi.FieldStorage()
product = form.getvalue("product")
#print(product)
orderid = form.getvalue("orderid")
if orderid is not None:
    orderid=int(orderid)

    
name = form.getvalue("name")

datestart = form.getvalue("datestart")
dateend = form.getvalue("dateend")
#dateend='03-20-2020'
#datestart='03-02-2020'
if datestart or dateend is not None:
    ds=datetime.datetime.strptime(datestart,'%Y-%m-%d')
    de=datetime.datetime.strptime(dateend,'%Y-%m-%d')
    ds = ds.date()
    de = de.date()
    delta=de-ds
    oneday= datetime.timedelta(days=1)
    zeroday= datetime.timedelta(days=0)
    #print(delta)



if product or name or orderid or datestart or dateend:
    connection = mysql.connector.connect(host="bioed.bu.edu",user='jiliu', password='jiliu', database='jiliu', port='4253')
    cursor = connection.cursor()
    print("<table id=miRNA>")
    print("<tr><th>id</th><th>person name</th><th>product</th><th>quantity</th><th>date</th></tr>")
    
    
    if product != 'Unknow' or name or orderid:
        if orderid is not None:
            query1= """SELECT Orders.id, Orders.person_name, Product.name, Orders.quantity, Orders.date 
            FROM Orders join Product on Orders.product_id=Product.id
            WHERE Product.name REGEXP '%s' OR Orders.person_name REGEXP '%s' OR Orders.id= %i;"""% (product,name,orderid)
            #print(query1)
            cursor.execute(query1)
            qone = cursor.fetchall()
            for row in qone:
                print("<tr><td>%i</td><td>%s</td><td>%s</td><td>%i</td><td>%s</td></tr>" % (row[0], row[1],row[2],row[3],row[4]))
                
        else:
            query2= """SELECT Orders.id, Orders.person_name, Product.name, Orders.quantity, Orders.date 
            FROM Orders join Product on Orders.product_id=Product.id
            WHERE Product.name REGEXP '%s' OR Orders.person_name REGEXP '%s';"""% (product,name)
            #print(query2)
            cursor.execute(query2)
            qtwo = cursor.fetchall()
            for row in qtwo:
                print("<tr><td>%i</td><td>%s</td><td>%s</td><td>%i</td><td>%s</td></tr>" % (row[0], row[1],row[2],row[3],row[4]))
                
    
        
            
        
    

    if datestart or dateend:

        
        # still need to use for loop to get every date from start to end
        while delta >= zeroday:
            delta = delta - oneday
            query3 = """SELECT Orders.id, Orders.person_name, Product.name, Orders.quantity, Orders.date 
            FROM Orders join Product on Orders.product_id=Product.id
            where Orders.date REGEXP '%s';""" %ds
            ds=ds+oneday
            cursor.execute(query3)
            qthree = cursor.fetchall()
            for row in qthree:
                print("<tr><td>%i</td><td>%s</td><td>%s</td><td>%i</td><td>%s</td></tr>" % (row[0], row[1],row[2],row[3],row[4]))
            


        
        
    #print("<p><font color=green><b>Success:</b> Order successfuly searched.</font></p>")
        
    print("</table>")
    cursor.close()    
    connection.close()
        
else:
    print("<p><font color=red><b>Error:</b> Please enter product, name, orderid or datestart, dateend.</font></p>")
        

	


#end the html code
print("""
</body>
</html>
""") 
