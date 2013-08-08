import requests, json, os
from lxml import html

HOST = 'http://maths:8080'

class LoginFailed(Exception):
    pass

# Log in
def emas_login(iUsername, iPassword):
    "Log into EMAS and return a session object"
    global HOST
    loginFormData = {
        "__ac_name": iUsername,
        "__ac_password": iPassword,
        "came_from": "",
        "next": "",
        "ajax_load": "",
        "ajax_include_head": "",
        "target": "",
        "mail_password_url": "",
        "join_url": "",
        "form.submitted": "1",
        "js_enabled": "0",
        "cookies_enabled": "",
        "login_name": "",
        "pwd_empty": "0",
        "submit": "Log in",
    }
    session = requests.Session()
    loginUrl = os.path.join(HOST, "login_form")
    loginResponse = session.post(loginUrl, data=loginFormData)
    if loginResponse.cookies.get('__ac') is None:
        raise LoginFailed, "EMAS authentication failed"
    return session

# Select a grade to practise
def select_grade(ioSession, iGrade):
    url = os.path.join(HOST, '@@practice/grade-' + str(iGrade))
    ioSession.get(url)

# Select a chapter
def select_chapter(ioSession, iChapterId):
    url = os.path.join(HOST, '@@practice/select_chapter', str(iChapterId))
    ioSession.get(url)

# Get a question
def get_question(ioSession):
    url = os.path.join(HOST, '@@practice/123/question')
    responseDom = html.fromstring(ioSession.get(url).content)
    node = responseDom.xpath('//*[@id="qa-dashboard"]')[0]
    templateId = int(node[0][0].tail)
    randomSeed = int(node[1][0].tail)
    subQuestionIndex = None
    expectedResponseCount = 0
    for node in responseDom.xpath('//*[@class="answer-input"]'):
        if (node.attrib.get('disabled') is None) and (node.attrib.get('readonly') is None):
            subQuestionIndex = int(node.attrib['name'][8:-1])-1
            expectedResponseCount += 1
    return templateId, randomSeed, subQuestionIndex, expectedResponseCount

# Get correct response from the oracle
def ask_oracle(ioSession, iTemplateId, iRandomSeed):
    url = os.path.join(HOST, '@@practice/oracle', str(iTemplateId), str(iRandomSeed))
    response = json.loads(ioSession.get(url).content)
    assert response['result'] == 'ok'
    return response['responses']

# Submit response to question
def submit_response(ioSession, iOracle, iSubQuestionIndex):
    url = os.path.join(HOST, '@@practice/submit_response')
    answers = iOracle[iSubQuestionIndex]
    postData = dict([('question' + str(iSubQuestionIndex+1) + chr(ord('a')+i), answers[i]) for i in range(len(answers))])
    ioSession.post(url, data=postData)

# Move on to next question
def next_question(ioSession):
    url = os.path.join(HOST, '@@practice/submit_response')
    postData = {'nextPage': 'Go to next question'}
    ioSession.post(url, data=postData)

# pull out csv of solutions using the oracle
def get_all_answers_from_oracle():
    # This method does not use the HTTP interface to request questions
    # and answers, saving *a lot* of overhead.
    import monassis.qnxmlservice as qnxml
    # get all template ids in db
    templateIds = qnxml.filter_templates()
    templateIds.sort()
    # for each template: request solution from oracle for seeds [0,1000]
    allResponses = {}
    for templateId in templateIds:
        print templateId
        templateResponses = []
        for randomSeed in range(1001):
            responses = []
            try:
                question = qnxml.request_question(templateId, randomSeed)
                for correctNode in question.dom.xpath('//response/correct'):
                    valueNodes = correctNode.findall('value')
                    if len(valueNodes) == 0:
                        responses.append([correctNode.text])
                    else:
                        responses.append([valueNode.text for valueNode in valueNodes])
            except Exception, e:
                print e.message, '(random seed: %i)'%randomSeed
            templateResponses.append(responses)
        allResponses[templateId] = templateResponses
    return allResponses

# Delete everything from template and media caches
def clear_all_caches():
    import subprocess
    p = subprocess.Popen(['./clean.sh'], cwd='src/monassis.qnxmlservice/monassis/qnxmlservice/template_cache')
    p.communicate()
    p = subprocess.Popen(['./clean.sh'], cwd='src/monassis.ploneserver/monassis/ploneserver/media')
    p.communicate()
