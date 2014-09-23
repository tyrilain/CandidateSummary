import os, pdb
from flask import render_template, jsonify, request
from app import app
import pymysql as mdb
from votesmart import votesmart
votesmart.apikey = '3735e7f15dceca1fb005baa0d6a7d717'

db = mdb.connect(user="root", host="localhost", db="VoteSmart", charset='utf8')

def getcandlist(con):
    # get current list of all candidates to populate search bar
    with con:
        cur = con.cursor()
        cur.execute('''
        SELECT distinct(fullname)
        FROM cand_tbl
        ''')
        data=cur.fetchall()
        print data
        dataarray=[]
        for cand in data:
            dataarray.append(cand[0].encode('ascii', 'ignore'))
            cur.close()
    return dataarray

def getcandID(con, candname):
    with con:
        cur = con.cursor()
        cur.execute('''
        SELECT candID
        FROM cand_tbl
        WHERE fullname='{}'
        '''.format(candname))
        data=cur.fetchall()
        print data
        cur.close()
#         dataarray=[]
#         for cand in data:
#             dataarray.append(cand[0].encode('ascii', 'ignore'))
#             cur.close()
    return str(data[0][0])


@app.route('/')
@app.route('/index')
@app.route('/zip')
def zip():
    ''' Home page with search for zip
    '''
    return render_template("zip.html")

# @app.route('/zipsearch', methods=['GET'])
# def showresults():
#     zip5 = request.args['zip']
#     if zip5 == '94404':
#         temp2 = [{u'electionOfficeId': u'5', u'suffix': u'', u'electionDistrictName': u'14', u'runningMateId': u'', u'officeStateId': u'', u'electionStatus': u'Running', u'electionStage': u'General', u'electionDate': u'2014-11-04', u'electionDistrictId': u'21192', u'title': u'', u'middleName': u'', u'officeDistrictName': u'', u'officeStatus': u'', u'officeTypeId': u'', u'electionOfficeTypeId': u'C', u'officeDistrictId': u'', u'nickName': u'', u'ballotName': u'Robin Chew', u'electionOffice': u'U.S. House', u'officeName': u'', u'runningMateName': u'', u'electionYear': u'2014', u'electionSpecial': u'f', u'preferredName': u'Robin', u'candidateId': u'146008', u'firstName': u'Robin', u'lastName': u'Chew', u'electionParties': u'Republican', u'officeId': u'', u'electionStateId': u'CA', u'officeParties': u''}, {u'electionOfficeId': u'5', u'suffix': u'', u'electionDistrictName': u'14', u'runningMateId': u'', u'officeStateId': u'CA', u'electionStatus': u'Running', u'electionStage': u'General', u'electionDate': u'2014-11-04', u'electionDistrictId': u'21192', u'title': u'U.S. House', u'middleName': u'Lorraine Jacqueline', u'officeDistrictName': u'14', u'officeStatus': u'active', u'officeTypeId': u'C', u'electionOfficeTypeId': u'C', u'officeDistrictId': u'14', u'nickName': u'Jackie', u'ballotName': u'Jackie Speier', u'electionOffice': u'U.S. House', u'officeName': u'U.S. House', u'runningMateName': u'', u'electionYear': u'2014', u'electionSpecial': u'f', u'preferredName': u'Jackie', u'candidateId': u'8425', u'firstName': u'Karen', u'lastName': u'Speier', u'electionParties': u'Democratic', u'officeId': u'5', u'electionStateId': u'CA', u'officeParties': u'Democratic'}]
#         cand_list = []
#         for cand in temp2:
#             mydict = {}
#             mydict['id'] = cand['candidateId']
#             mydict['name'] = cand['preferredName']+' '+cand['lastName']
#             mydict['party'] = cand['electionParties']
#             if cand['electionDistrictName']:
#                 mydict['office'] = "%s Dist %s, %s" % (cand['electionOffice'], cand['electionDistrictName'], cand['electionStateId'])
#             else:
#                 mydict['office'] = "%s, %s" % (cand['electionOffice'], cand['electionStateId'])
#             cand_list.append(mydict)
#     else:
#         temp = votesmart.candidates.getByZip(zip5)
#         # Filtering for congressional candidates
#         temp2 = [x for x in temp if (x.electionOfficeTypeId == 'C' and x.electionStatus == 'Running')]
#         cand_list = []
#         for cand in temp2:
#             mydict = {}
#             mydict['id'] = cand.candidateId
#             mydict['name'] = cand.preferredName+' '+cand.lastName
#             mydict['party'] = cand.electionParties
#             if cand.electionDistrictName:
#                 mydict['office'] = "%s Dist %s, %s" % (cand.electionOffice, cand.electionDistrictName, cand.electionStateId)
#             else:
#                 mydict['office'] = "%s, %s" % (cand.electionOffice, cand.electionStateId)
#             cand_list.append(mydict)
#     return render_template("zip.html", cands=cand_list)

@app.route('/zipsearch')
def showresults():
    zip5 = request.args['zip']
    if zip5 == '94404':
        temp2 = [{u'electionOfficeId': u'5', u'suffix': u'', u'electionDistrictName': u'14', u'runningMateId': u'', u'officeStateId': u'', u'electionStatus': u'Running', u'electionStage': u'General', u'electionDate': u'2014-11-04', u'electionDistrictId': u'21192', u'title': u'', u'middleName': u'', u'officeDistrictName': u'', u'officeStatus': u'', u'officeTypeId': u'', u'electionOfficeTypeId': u'C', u'officeDistrictId': u'', u'nickName': u'', u'ballotName': u'Robin Chew', u'electionOffice': u'U.S. House', u'officeName': u'', u'runningMateName': u'', u'electionYear': u'2014', u'electionSpecial': u'f', u'preferredName': u'Robin', u'candidateId': u'146008', u'firstName': u'Robin', u'lastName': u'Chew', u'electionParties': u'Republican', u'officeId': u'', u'electionStateId': u'CA', u'officeParties': u''}, {u'electionOfficeId': u'5', u'suffix': u'', u'electionDistrictName': u'14', u'runningMateId': u'', u'officeStateId': u'CA', u'electionStatus': u'Running', u'electionStage': u'General', u'electionDate': u'2014-11-04', u'electionDistrictId': u'21192', u'title': u'U.S. House', u'middleName': u'Lorraine Jacqueline', u'officeDistrictName': u'14', u'officeStatus': u'active', u'officeTypeId': u'C', u'electionOfficeTypeId': u'C', u'officeDistrictId': u'14', u'nickName': u'Jackie', u'ballotName': u'Jackie Speier', u'electionOffice': u'U.S. House', u'officeName': u'U.S. House', u'runningMateName': u'', u'electionYear': u'2014', u'electionSpecial': u'f', u'preferredName': u'Jackie', u'candidateId': u'8425', u'firstName': u'Karen', u'lastName': u'Speier', u'electionParties': u'Democratic', u'officeId': u'5', u'electionStateId': u'CA', u'officeParties': u'Democratic'}]
        cand_list = []
        for cand in temp2:
            mydict = {}
            mydict['id'] = cand['candidateId']
            mydict['name'] = cand['preferredName']+' '+cand['lastName']
            mydict['party'] = cand['electionParties']
            if cand['electionDistrictName']:
                mydict['office'] = "%s Dist %s, %s" % (cand['electionOffice'], cand['electionDistrictName'], cand['electionStateId'])
            else:
                mydict['office'] = "%s, %s" % (cand['electionOffice'], cand['electionStateId'])
            cand_list.append(mydict)
    else:
        temp = votesmart.candidates.getByZip(zip5)
        # Filtering for congressional candidates
        temp2 = [x for x in temp if (x.electionOfficeTypeId == 'C' and x.electionStatus == 'Running')]
        cand_list = []
        for cand in temp2:
            mydict = {}
            mydict['id'] = cand.candidateId
            mydict['name'] = cand.preferredName+' '+cand.lastName
            mydict['party'] = cand.electionParties
            if cand.electionDistrictName:
                mydict['office'] = "%s Dist %s, %s" % (cand.electionOffice, cand.electionDistrictName, cand.electionStateId)
            else:
                mydict['office'] = "%s, %s" % (cand.electionOffice, cand.electionStateId)
            cand_list.append(mydict)
    return jsonify(dict(cands=cand_list))


@app.route("/candidate", methods=['GET'])
def find_candidate():
    cand_dict = {}
    candname = request.args['CandName']
    cand_id = getcandID(db,candname)
    with db:
        cur = db.cursor()
        cur.execute("SELECT party, office, state, district FROM cand_tbl WHERE candID = %s;", cand_id)
        query_results = cur.fetchall()
        cur.close()
    print query_results[0]
    cand_dict['name'] = candname
    cand_dict['id'] = cand_id
    cand_dict['party'] = query_results[0][0]
    cand_dict['office'] = query_results[0][1]
    cand_dict['state'] = query_results[0][2]
    cand_dict['district'] = query_results[0][3]
    
    return render_template("result.html", cand=cand_dict)
    

# poplist was used to auto-complete a dropdown list of candidates, now defunct    
@app.route('/poplist',methods=['GET'])
def poplist():
    output={}
    output['data']=getcandlist(db)
    print output['data']
    return jsonify(output)


def index_jquery():
    return render_template('result.html', candID='0') 
    
@app.route('/<int:candID>')
def show_cand(candID):
    cand_dict = {}
    cand_id = candID
    with db:
        cur = db.cursor()
        cur.execute("SELECT party, office, state, district, fullname FROM cand_tbl WHERE candID = %s;", cand_id)
        query_results = cur.fetchall()
        cur.close()
    print query_results[0]
    cand_dict['name'] = query_results[0][4]
    cand_dict['id'] = cand_id
    cand_dict['party'] = query_results[0][0]
    cand_dict['office'] = query_results[0][1]
    cand_dict['state'] = query_results[0][2]
    cand_dict['district'] = query_results[0][3]
    
    return render_template("result.html", cand=cand_dict)
# 
#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT Name FROM candidate_tbl WHERE candID = 100;")
#         query_results = cur.fetchall()
#         cur.close()
# #    bio = []
# #    for result in query_results:
# #        bio.append(dict(name=result[0], country=result[1], population=result[2]))
# 
#     return render_template('result.html', candID = query_results[0][0])

@app.route('/db')
def cities_page():
    with db: 
        cur = db.cursor()
        cur.execute("SELECT Name FROM city LIMIT 15;")
        query_results = cur.fetchall()
    cities = ""
    for result in query_results:
        cities += result[0]
        cities += "<br>"
    return cities

@app.route("/db_fancy")
def cities_page_fancy():
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM city ORDER BY Population LIMIT 15;")

        query_results = cur.fetchall()
    cities = []
    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))
    return render_template('cities.html', cities=cities) 
