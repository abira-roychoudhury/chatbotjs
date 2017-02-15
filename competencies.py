import logging
import os
import MySQLdb

def getCompetencies(employeeId, db, subordinateId=None):
	logging.info("Inside getCompetencies()")

	cursor = db.cursor()	

	logging.info("cursor built")

	if subordinateId :
		logging.info("|"+str(employeeId)+"|")
		cursor.execute("SELECT COUNT(*) FROM UserMaster U WHERE U.ReportingManagerID = '%d' AND U.EmpCode = '%s'" % ( int(employeeId), str(subordinateId) ))

		count = cursor.fetchone()

		if count[0] < 1:
			return "This employeee is not your subordiante"
		else:
			employeeId = subordinateId


	cursor1 = db.cursor()	
	#cursor2 = db.cursor()	
	#cursor3 = db.cursor()

	cursor1.execute("SELECT C.CompetencyID, C.DesiredLevelID, C.EmpCompetencyID FROM EmployeeCompetency C, UserMaster U WHERE U.EmpCode = '%s' AND C.EmpID = U.UserID AND C.AppraisalCycleID = 12" % (str(employeeId)))

	count = cursor1.rowcount

	if count < 1:
		return "Competency is not set"
	else:
		result1 = cursor1.fetchall()
		speech = "These are the competencies<br>\
					<table>\
						<tr>\
							<th>ID</th>\
							<th>Title</th>\
							<th>Desired Level</th>\
						</tr>"

		for row in result1:

			cursor1.execute("SELECT Title FROM CustomerCompetencyMaster WHERE CompetencyID = '%d'" % (int(row[0])))
			result2 = cursor1.fetchone()
			
			#query = "SELECT ARM.Rating FROM EmployeeCompetencyRatings ECR, AppraisalRatingMaster ARM WHERE ECR.RatingID = ARM.AppraisalRatingsID AND ECR.EmpCompetencyID = '%d'" % (int(row[2]))
			#cursor1.execute(query)
			#result3 = cursor1.fetchone()
			
			logging.info("competencyID: "+ str(row[2]))

			#logging.info("result3 :"+str(result3))
			#logging.info(result3)

			speech = speech + "\
				<tr>\
					<td>"+str(int(row[2]))+"</td>\
					<td>"+str(result2[0])+"</td>\
					<td>Level "+str(row[1])+"</td>\
				</tr>"
				
		speech = speech + "</table><br>Enter the ID whose details you want to see"

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
							Enter the Employee code of the subordinate, whose competencies you want to see"
									
		return speech


def getCompetencies_details(EmpCompetencyID, db):

	logging.info("Inside getCompetencies()")

	cursor = db.cursor()	

	logging.info("cursor built")

	query = "SELECT ARM.Rating FROM EmployeeCompetencyRatings ECR, AppraisalRatingMaster ARM WHERE ECR.RatingID = ARM.AppraisalRatingsID AND ECR.EmpCompetencyID = '%d'" % (int(EmpCompetencyID))
	cursor.execute(query)
	count = cursor.rowcount
	
	logging.info("count :"+str(count))

	if count < 1:
		speech = "There are no ratings available for this competency"
	else:
		result = cursor.fetchone()

		logging.info("result :"+str(result))
		logging.info(result)

		speech = "Ratings : "+str(result[0])

	query = "SELECT SelfComments FROM EmployeeCompetencySelfComments WHERE EmpCompetencyID = '%d'" % (int(EmpCompetencyID))
	cursor.execute(query)
	count = cursor.rowcount

	if count < 1:
		speech = speech + "<br>There are no self comments available for this competency"
	else:
		result = cursor.fetchone()

		logging.info("result :"+str(result))
		logging.info(result)

		speech = speech +"<br>Self Comments : "+str(result[0])

	
	return speech
