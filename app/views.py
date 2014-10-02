import os, pdb
from flask import render_template, jsonify, request
from app import app, load_db
# import pymysql as mdb
from votesmart import votesmart
votesmart.apikey = '3735e7f15dceca1fb005baa0d6a7d717'
import ftfy

def getcandlist():
    ''' Get current list of all candidates to populate search bar
    '''
    db = load_db.DB()
    cur = db.cur
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
    con.close()
    return dataarray

def getcandID(candname):
    ''' Search for candidate ID by candidate name.
    '''
    db = load_db.DB()
    cur = db.cur
    cur.execute('''
        SELECT candID
        FROM cand_tbl
        WHERE fullname='{}'
        '''.format(candname))
    data=cur.fetchall()
    print data
    cur.close()
    con.close()
    return str(data[0][0])


@app.route('/')
@app.route('/index')
@app.route('/zip')
def zip():
    ''' Home page with search for zip
    '''
    return render_template("zip.html")

@app.route('/slides')
def slides():
    ''' Slides
    '''
    return render_template("slides.html")


@app.route('/zipsearch')
def showresults():
    ''' Get list of candidates in zip from VoteSmart API, or use cached example
        (94404).
    '''
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

@app.route('/<int:candID>')
def show_cand(candID):
    ''' Display candidate summary page given candidate ID.
    '''
    cand_dict = {}
    cand_id = candID
    
    # query database for profile info
    db = load_db.DB()
    db.query("SELECT party, office, state, district, fullname FROM cand_tbl WHERE candID = %s;", cand_id)
    query_results = db.cur.fetchall()
    db.cur.close()
#     print query_results[0]
    
    # save results to populate webpage
    cand_dict['name'] = query_results[0][4]
    cand_dict['id'] = cand_id
    cand_dict['party'] = query_results[0][0]
    cand_dict['office'] = query_results[0][1]
    cand_dict['state'] = query_results[0][2]
    cand_dict['district'] = query_results[0][3]
    
    # query database for bigram info
    db = load_db.DB()
    db.query("SELECT b1, b2, b3, b4, b5, b6, b7, b8 FROM bigrams_tbl WHERE id = %s;", cand_id)
    query_results = db.cur.fetchall()
    db.cur.close()

    cand_dict['bigrams'] = list(query_results[0])
#     ['private sector',
#                               'bay area',
#                                 'climate change',
#                                 'hong kong',
#                                 'old saying',
#                                 'united states',
#                                 'burdensome regulations',
#                                 'international trade']
    cand_dict['quotes'] = ['Many of the flood of asylum seekers are minors sent north by parents who despair for their children&#39;s future in violence-ridden Central American countries like El Salvador, Guatemala and Honduras.',
                            'Mexico won&#39;t stop them, and, in fact, President Enrique Pena Nieto on Monday announced plans to help guarantee their safety and effectively facilitate their transit northward.',
                            'If you decide to write that check to an out of state politician, remember next time you are complaining about local incumbent Democrats, be prepared to accept your share of responsibility because you didn&#39;t support candidates here at home.',
                            'This burden is a terrible legacy to leave to our children, and the harm is compounded by the fact that this debt puts downward pressure on our economy, costing us the jobs and spending that could fuel a robust recovery.',
                            'As a Congressman, my signature legislative agenda will be a reprioritizing and reimagining of our nation&#39;s infrastructure: modern roads and clean, efficient transportation, rebuilt bridges, secure electrical grids and renewable energy.']
    cand_dict['quotes'] = [ftfy.fix_text(unicode(quote)) for quote in cand_dict['quotes']]


    return render_template("result.html", cand=cand_dict)

@app.route("/candidate", methods=['GET'])
def find_candidate():
    ''' Used to pull result page given a candidate name. (Deprecated)
    '''
    cand_dict = {}
    candname = request.args['CandName']
    cand_id = getcandID(candname)
    db = load_db.DB()
    db.querry("SELECT party, office, state, district FROM cand_tbl WHERE candID = %s;", cand_id)
    query_results = db.cur.fetchall()
    db.cur.close()
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
    output['data']=getcandlist()
    print output['data']
    return jsonify(output)
