from enum import Enum
import mysql.connector
import pyodbc
import pandas

class DatabaseType(Enum):
    MySql = 1
    MsSqlServer = 2

class SqlExecutionResults(object):
    def __init__(self):
        self.hasError = False
    
    def ExecutionResult(self, results):
        self.executionResult = results
    
    def ExecutionError(self, error):
        self.hasError = True
        self.executionError = error

class SqlUser(object):
    def __init__(self, databaseType, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.databaseType = databaseType

    def TestConnection(self):
        returnValue = SqlExecutionResults()
        try:
            if self.databaseType == DatabaseType.MySql:
                self.sqlConnection = mysql.connector.connect(user=self.user, password=self.pwd, host=self.host)
            elif self.databaseType == DatabaseType.MsSqlServer:
                self.sqlConnection = pyodbc.connect("DSN=" + self.host + ";UID=" + self.user + ";PWD=" + self.pwd + ";")
        except (mysql.connector.Error, pyodbc.Error) as connectionError:
            returnValue.ExecutionError(connectionError)
        finally:
            return returnValue
    
    def Close(self):
        self.sqlConnection.Close()

    def ExecuteRead(self, query):
        returnValue = SqlExecutionResults()
        try:
            returnValue.ExecutionResult(pandas.read_sql(query, self.sqlConnection))
        except (mysql.connector.Error, pyodbc.Error) as connectionError:
            returnValue.ExecutionError(connectionError)
        finally:
            return returnValue

    def ExecuteWrite(self, query):
        returnValue = SqlExecutionResults()
        self.sqlCursor = self.sqlConnection.cursor()
        try:
            self.sqlCursor.execute(query)
            self.sqlConnection.commit()
        except (mysql.connector.Error, pyodbc.Error) as connectionError:
            returnValue.ExecutionError(connectionError)
        finally:
            return returnValue