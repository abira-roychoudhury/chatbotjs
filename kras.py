import logging
import os
import MySQLdb

def checkUser(firstname, lastname, employeeId, db):
	logging.info("Inside checkUser()")

	cursor = db.cursor()

	logging.info("cursor built")
	cursor.execute("SELECT * FROM UserMaster WHERE FirstName = '%s' AND LastName = '%s' AND EmpCode = '%s'" % (firstname, lastname, employeeId))

	logging.info("query executed")
	count = cursor.rowcount

	logging.info("rowcount fetched")
	logging.info("count: "+str(count))

	if count > 0:
		return True
	else :
		return False


def getKras(employeeId, db, subordinateId=None):
	logging.info("Inside getKras()")

	cursor = db.cursor()	

	logging.info("cursor built")

	if subordinateId :
		cursor.execute("SELECT COUNT(*) FROM UserMaster U WHERE U.ReportingManagerID = '%d' AND U.EmpCode = '%s'" % ( int(employeeId), str(subordinateId) ))

		count = cursor.fetchone()

		if count[0] < 1:
			return "This employeee is not your subordiante"
		else:
			employeeId = subordinateId


	cursor.execute("SELECT K.EmpKRAID, K.KRATitle, K.Weight FROM EmployeeKRA K, UserMaster U WHERE U.EmpCode = '%s' AND K.EmpID = U.UserID" % (str(employeeId)))

	count = cursor.rowcount

	if count < 1:
		return "KRA is not set"
	else:
		results = cursor.fetchall()
		speech = "These are the KRA titles<br>\
					<table>\
						<tr>\
							<th>KRAID</th>\
							<th>Title</th>\
							<th>Weight</th>\
						</tr>"

		for row in results:

			speech = speech + "\
				<tr>\
					<td>"+str(row[0])+"</td>\
					<td>"+str(row[1])+"</td>\
					<td>"+str(row[2])+"</td>\
				</tr>"
				
		speech = speech + "</table><br>\
							Enter the KRAID whose details you want to see"

		return speech


def getSubordinates(employeeId, db):
	logging.info("Inside getSubordinates()")

	cursor = db.cursor()	

	logging.info("cursor built")

	cursor.execute("SELECT EmpCode, FirstName, LastName FROM UserMaster U WHERE U.ReportingManagerID = '%d'" % ( int(employeeId) ))

	count = cursor.rowcount

	if count < 1:
		return "You dont have any subordinates"
	else:
		results = cursor.fetchall()
		speech = "These are your subordinates: <br>\
					<table>"
		for row in results:
			speech = speech + "<tr>\
								<td>"+str(row[0])+"</td>\
								<td>"+str(row[1])+" "+str(row[2])+"</td>\
							</tr>"

		speech = speech + "</table>\
							Enter the Employee code of the subordinate, whose KRA you want to see"
									
		return speech



def getKraDescription(KRAID, choice, whose, db):
	logging.info("Inside getKraDescription()")

	cursor = db.cursor()	

	logging.info("cursor built")
	logging.info("KRAID :" + str(KRAID))
	logging.info("choice :" + str(choice))
	logging.info("type of KRAID :" + str(type(KRAID)))

	if choice == "description":
		cursor.execute("SELECT Description FROM EmployeeKRA WHERE EmpKRAID = '%d'" % (int(KRAID)))
	elif choice == "ratings":

		query = "SELECT ARM.Rating FROM EmployeeKRA EK, EmployeeKRARatings EKR, AppraisalRatingMaster ARM WHERE EK.EmpKRAID = EKR.EmpKRAID AND EKR.RatingID = ARM.AppraisalRatingsID AND EK.EmpKRAID = '%d'" % (int(KRAID))
		cursor.execute(query)

	elif choice == "self comment" :

		query = "SELECT SelfComments FROM EmployeeKRASelfComments WHERE EmpKRAID = '%d'" % (int(KRAID))
		cursor.execute(query)
	elif choice == "manager comment":
		cursor.execute()
	else:
		return "Incorect Choice"

	count = cursor.rowcount

	if count < 1:
		speech = str(choice)+" not assigned for this KRAID"
	else:
		results = cursor.fetchall()
		speech = "KRA "+choice.title()+" : <br> "

		for row in results:
			speech = speech + str(row[0])

		if (whose == 'me' or whose == 'my' or whose == 'mine' or whose == 'myself') and choice == 'self comment':
			speech = speech + "<br><br>Do you want to update the "+str(choice)+"?"
		elif whose == 'subordinate' and choice != 'self comment' :
			speech = speech + "<br><br>Do you want to update the "+str(choice)+"?"

	logging.info(speech)
	return speech


def updateKRA(KRAID, choice, newValue, db):
	logging.info("Inside updateKRA()")

	cursor = db.cursor()	

	logging.info("cursor built")
	logging.info("KRAID :" + str(KRAID))
	logging.info("choice :" + str(choice))
	logging.info("type of KRAID :" + str(type(KRAID)))
	logging.info("newValue:"+ str(newValue))

	if choice == "description":	
		try:
			cursor.execute("UPDATE EmployeeKRA set Description = '%s' WHERE EmpKRAID = '%d'" % (str(newValue), int(KRAID)))
			db.commit()
		except :
			db.rollback()
			return "Unable to update the Description"

	elif choice == "ratings":
		try:
			query = "SELECT ARM.AppraisalRatingsID FROM EmployeeKRA EK, EmployeeKRARatings EKR, AppraisalRatingMaster ARM WHERE EK.EmpKRAID = EKR.EmpKRAID AND EKR.RatingID = ARM.AppraisalRatingsID AND EK.EmpKRAID = '%d'" % ( int(KRAID))
			cursor.execute(query)
			
			results = cursor.fetchone()
			
			logging.info("results :"+str(results))

			query2 = "UPDATE AppraisalRatingMaster set Rating = '%d' WHERE AppraisalRatingsID = '%d'" % (int(newValue),int(results[0]))

			cursor = db.cursor()
			cursor.execute(query2)

			db.commit()
		except:
			db.rollback()
			return "Unable to update the Rating"

	elif choice == "self comment" :
		try:
			query = "UPDATE EmployeeKRASelfComments SET SelfComments = '%s' WHERE EmpKRAID = '%d'" % (str(newValue), int(KRAID))
			cursor.execute(query)
			db.commit()
		except:
			db.rollback()
			return "Unable to update the Self Comments"

	elif choice == "manager comment":
		try:
			query = ""
			cursor.execute(query)
			db.commit()
		except:
			db.rollback()
			return "Unable to update the Manager's Comments"

	else:
		return "Incorect Choice"

	return choice.title() + " updated successfully to "+str(newValue)
