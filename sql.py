import mysql.connector
import random

mydb = mysql.connector.connect(
    host ="localhost",
    user ="root",
    passwd ="deepanshu10"
)
mycursor=mydb.cursor()


def initiate():
    mycursor.execute("CREATE DATABASE INFORMATION")
    print("[SERVER]: DATABASE CREATED")

    mycursor.execute("USE INFORMATION")
    for i in ["PHYSICS","CHEMISTRY","MATHS"]:
        mycursor.execute(f"CREATE TABLE {i} (ID char(7), CHAPTER varchar(10), LEVEL char(10), QUESTION varchar(1000), Option_A varchar(1000), Option_B varchar(1000), Option_C varchar(1000), Option_D varchar(1000), ANSWER char(2), PRIMARY KEY(id))")
    mycursor.execute("CREATE TABLE USERDATA (USERNAME char(100), PASSWORD char(100), EMAIL char(100), PRIMARY KEY(email))")
    print("[SERVER]: DATABASE STARTED")
def delete():
    mycursor.execute("DROP DATABASE INFORMATION")
    print("[SERVER]: DATABASE DELETED")



def insert(sub,chap,lvl,ques,opt,ans):
    #Insert new question
    ID="@"+str(sub[0])+str(lvl[0])+str(random.randint(1000,9999))
    print(ID,sub,chap,lvl,ques,opt,ans)
    mycursor.execute(f"INSERT INTO {sub} VALUES('{ID}','{chap}','{lvl}','{ques}','{opt[0]}','{opt[1]}','{opt[2]}','{opt[3]}','{ans}')")
    mydb.commit()
    print("[SERVER]: INSERTED")
def result(sub,chap,lvl):
    #Gives output
    mycursor.execute(f'select QUESTION, OPTION_A, OPTION_B, OPTION_C, OPTION_D from {sub} where CHAPTER IN {tuple(chap)} and LEVEL="{lvl}" ORDER BY RAND() LIMIT 15;')
    answer=mycursor.fetchall()
    return answer
def createpaper():
    final={}
    for x in ["PHYSICS","CHEMISTRY","MATHS"]:
        mycursor.execute(f'select ID, QUESTION, OPTION_A, OPTION_B, OPTION_C, OPTION_D from {x} ORDER BY RAND() LIMIT 25;')
        answer=mycursor.fetchall()
        final[x]=answer
    return final
def anything(any):
    mycursor.execute(f'{any}')
    answer=list(mycursor.fetchone())[0]
    return answer    



def user_insert(usnm,pswd,email):
    #Insert new user
    mycursor.execute(f"INSERT INTO USERDATA VALUES('{usnm}','{pswd}','{email}')")
    mydb.commit()
def maintain(usnm,pswd):
    #Verify sign-in
    try:
        mycursor.execute(f'select * from USERDATA where email="{usnm}"')
        myresult=mycursor.fetchone()
        if myresult[1]==pswd:
            return ("Verified",myresult[0])
        else:
            return ("Failed")
    except:
        return "Failed"

    
#delete()
try:
    initiate()
except:
    mycursor.execute("USE INFORMATION")
