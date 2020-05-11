#!/usr/bin/env python

import mysql.connector
import datetime
import string
import random


class Db():

    def __init__(self):
        self.mydb_r = mysql.connector.connect(
            host="db-rw",
            port=3306,
            user="root",
            passwd="sam@sam",
            database="buytradedb"
        )
        self.mycursor_r = self.mydb_r.cursor()
        self.mydb_rw = mysql.connector.connect(
            host="db-rw",
            port=3306,
            user="root",
            passwd="sam@sam",
            database="buytradedb"
        )
        self.mycursor_rw = self.mydb_rw.cursor()

    def createTable(self):

        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS `user` ( `ID` INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, `UserName` VARCHAR(30) NOT NULL , `Email` VARCHAR(50) NOT NULL , `Password` VARCHAR(10) NOT NULL , `Address` VARCHAR(500) NULL , `ContactNo` BIGINT(15) NULL , `CreatedDate` DATETIME NOT NULL ) ENGINE = InnoDB;")

        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS `tokens` (`id` INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, `user_id` INT(6) , `token` VARCHAR(50)  )")

    def do_login(self, username, password, check=False):
        # self.createTable()
        sql = "SELECT * FROM user WHERE UserName = %s AND Password = %s"
        param = (username, password)

        self.mycursor_r.execute(sql, param)
        myresult = self.mycursor_r.fetchall()

        print('length of array')
        print(len(myresult))
        print(myresult)
        # exit(0)
        if len(myresult) < 1:
            return False

        token = ''.join(random.choices(string.ascii_uppercase +
                                       string.digits, k=40))
        if check == False:
            # Remove existed token
            delete = "DELETE FROM tokens WHERE user_id = " + str(myresult[0][0])
            self.mycursor_r.execute(delete)

            self.mydb_r.commit()
            # Login successful
            sql = "INSERT INTO tokens (`ID`,`user_id`,`token`) VALUES(NULL,%s,%s)"
            param = (myresult[0][0], token)

            self.mycursor_r.execute(sql, param)
            self.mydb_r.commit()

        return token

    def do_registration(self, object):
        UserName = object['UserName']
        Email = object['Email']
        Password = object['Password']
        Address = object['Address']
        ContactNo = object['ContactNo']

        # check if user is already exits
        response = self.do_login(UserName, Password, check=True)
        if response != False:
            return False

        sql = "INSERT INTO user (`ID`,`UserName`,`Email`,`Password`,`Address`,`ContactNo`,`CreatedDate`) VALUES(NULL,%s,%s,%s,%s,%s,NOW())"
        param = (UserName, Email, Password, Address,
                 ContactNo)

        self.mycursor_rw.execute(sql, param)
        self.mydb_rw.commit()

        return True
