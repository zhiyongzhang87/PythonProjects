import SqlTools as SqlTools

databaseType = SqlTools.DatabaseType.MySql
sqlConnection = SqlTools.SqlUser(databaseType, "127.0.0.1", "zhiyong", "Zhzhy@0809")
connectionTestResult = sqlConnection.TestConnection()
if connectionTestResult.hasError == False:
    query = "INSERT INTO Test.tblTest VALUES ('20180716',2);"
    results = sqlConnection.ExecuteWrite(query)
    if results.hasError == True:
        print (results.executionError)
    else:
        results = sqlConnection.ExecuteRead("SELECT * FROM Test.tblTest;")
        if results.hasError == True:
            print (results.executionError)
        else:
            print (results.executionResult.head())
else:
    print ("Database connection error:")
    print (connectionTestResult.executionError)