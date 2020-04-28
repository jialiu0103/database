#!/usr/local/Python-3.7/bin/python3
import pymysql
import cgi
#print("Content-type: text/html\n") 
# retrieve form data, if any
form = cgi.FieldStorage()

#check if form data is returned
if form:

    # Connect to the database.
    connection = pymysql.connect(host='bioed.bu.edu',database='jiliu',user='jiliu',password='jiliu',port=4253)
    cursor = connection.cursor()

    # check if submit button was clicked
    submit = form.getvalue("submit")
    flag= form.getvalue("flag")
    
    
    if submit:
        #get the pathway
        products_name = form.getvalue("products_name")
        
        
        #specify the query for the interacting proteins
        query = '''
        SELECT products_name, price, quantity
        FROM products 
        WHERE products_name = '%s' 
        '''%(products_name)
        
        #execute the query
        cursor.execute(query)
        rows=cursor.fetchall()
        
        
        #start http return 
        print("Content-type: text/html\n")
        
        #print the rows of the response
        for row in rows:
            if float(row[1]):
                ls=[]
                ls.append(row[0])
                ls.append(str(row[1]))
                ls.append(str(row[2]))
                ls=",".join(ls)
                print(ls)
            else: 
                if float(row[2]):
                    name=row[0] + ' ' + row[1]
                    ls=[]
                    ls.append(name)
                    ls.append(str(row[2]))
                    ls.append(str(row[3]))
                    ls=",".join(ls)
                    print(ls)
                else:
                    if float(row[3]):
                        name=row[0] + ' ' + row[1] + ' ' + row[2]
                        ls=[]
                        ls.append(name)
                        ls.append(str(row[3]))
                        ls.append(str(row[4]))
                        ls=",".join(ls)
                        print(ls)
                    else:
                        if float(row[4]):
                            name=row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3]
                            ls=[]
                            ls.append(name)
                            ls.append(str(row[4]))
                            ls.append(str(row[5]))
                            ls=",".join(ls)
                            print(ls)
                        else:
                            if float(row[5]):
                                name=row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4]
                                ls=[]
                                ls.append(name)
                                ls.append(str(row[5]))
                                ls.append(str(row[6]))
                                ls=",".join(ls)
                                print(ls)
                            else:
                                name=row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4] + ' ' + row[5]
                                ls=[]
                                ls.append(name)
                                ls.append(str(row[6]))
                                ls.append(str(row[7]))
                                ls=",".join(ls)
                                print(ls)
    

        
        
    #otherwise, one of the drop down menus was clicked
    else:
        table = form.getvalue("table")

        #specify the query for the gene table
        if (table == "categories"):
            query = '''
            SELECT categories_name 
            FROM categories
            '''
        if (table == "products"):
                categories_name = form.getvalue("categories_name")      
                query = '''
                SELECT products_name 
                FROM products join categories using(cid) 
                WHERE categories_name = '%s'
                '''%(categories_name)

        
        
        
        #execute the query
        
        cursor.execute(query)
        rows=cursor.fetchall()
        
        
       

        #start http return 
        print("Content-type: text/html\n")
        #print the rows of the response
        for row in rows:
            print(row[0])

else:
    #no form data, just print an empty http header
    print("Content-type: text/html\n")
    print('no cgi link here')
    
 

