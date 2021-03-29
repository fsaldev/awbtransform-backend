import base64
import json
import os
from datetime import datetime
from multiprocessing import process
from flask import Flask, request, jsonify, render_template, make_response, send_file, send_from_directory
from flask_cors import cross_origin
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import pdfkit
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['MONGODB_SETTINGS'] = {
    'db': 'awbtransport',
    'host': 'mongodb+srv://test:test1234@test.iocw1.mongodb.net/awbTransport1',
    # 'db': 'awbtransport',
    # 'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
PDFKIT_CONFIGURATION  = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
# PDFKIT_CONFIGURATION = pdfkit.configuration(wkhtmltopdf="/home/awbtransport/wkhtml-install/usr/local/bin/wkhtmltopdf")

######################################Start Models########################################################


class EmploymentHistory(db.EmbeddedDocument):
    employmentHistoryfrom = db.DateField()
    employmentHistoryTo = db.DateField()
    employmentHistorystatus = db.StringField()
    employmentHistoryposition = db.StringField()
    employmentHistoryaddress = db.StringField()
    employmentHistorycompanyPhone = db.StringField()
    employmentHistoryreasonForLeaving = db.StringField()
    employmentHistorysubjecttotheFMCSRs = db.StringField()
    employmentHistorydrugandalcoholTesting = db.StringField()

class Experience(db.EmbeddedDocument):
    experienceclassofEquipment = db.StringField()
    experienceFromDate = db.DateField()
    experienceToDate = db.DateField()
    experiencenumberOfMiles = db.StringField()

class Accident(db.EmbeddedDocument):
    dateOfAccident = db.DateField()
    NumberOfAccidents = db.StringField()
    LocationOfAccidents = db.StringField()
    numberofFatalities = db.StringField()
    numberofPeopleleInjured= db.StringField()

class TrafficViolations(db.EmbeddedDocument):
    dateOfViolation = db.DateField()
    LocationOfViolation = db.StringField()
    ViolationCharge = db.StringField()
    ViolationPenalty = db.StringField()

class Address(db.EmbeddedDocument):
    lastYearAddress = db.StringField()
    lastYearAddressCity = db.StringField()
    lastYearAddressState = db.StringField()
    lastYearAddressZipCode = db.StringField()
    lastYearAddressfrom = db.DateField()
    lastYearAddressTo = db.DateField()

class Resume(db.EmbeddedDocument):
    file_name = db.StringField()

class Licence(db.EmbeddedDocument):
    stateOfLicence = db.StringField()
    licenceNumber = db.StringField()
    licenceType = db.StringField()
    licenceEndoresment = db.StringField()
    licenceExpirationDate = db.DateField()

class Reference(db.EmbeddedDocument):
    referencefirstName = db.StringField()
    referencelastName = db.StringField()
    referenceCompany = db.StringField()
    referenceTitle = db.StringField()
    referencePhoneNumber = db.StringField()
    referenceAddress = db.StringField()
    referenceCity = db.StringField()
    referenceState = db.StringField()
    referenceZipCode = db.StringField()

class DriversData(db.Document):
    user_name = db.StringField()
    password = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    email = db.StringField()
    dateofBirth = db.DateField()
    socialSecurity = db.StringField()
    address = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zipCode = db.StringField()
    fromDateAddress = db.DateField()
    lastThreeYearResidenceCheck = db.StringField()
    maritial_status = db.StringField()
    NumberofDependantsUnder17 = db.IntField()
    NumberofDependantsOver17 = db.IntField()

    #documents
    resume = db.StringField()
    dodMedicalCardFile = db.StringField()
    dmvFile = db.StringField()
    driverLicenceFile = db.StringField()

    #lastyearaddressses
    addresses = db.ListField(db.EmbeddedDocumentField(Address))

    startTime = db.StringField()
    hearAbout = db.StringField()
    eligibletoWorkInUnitedState = db.StringField()
    classAExperienceLevel = db.StringField()
    willingForDrugTest = db.StringField()
    gender = db.StringField()
    veteranStatus = db.StringField()

    #ComapnyInformation
    companyName = db.StringField()
    companyAddress = db.StringField()
    companyCity = db.StringField()
    companyState = db.StringField()
    companyPostCode = db.StringField()

    #applicantinfo
    applicationApplyDate = db.DateField()
    applicationApplyAsPosition = db.StringField()
    applicantfirstName = db.StringField()
    applicantLastName = db.StringField()
    applicantPhoneNumber = db.StringField()
    emergencyContactfirstName = db.StringField()
    emergencyContactlastName = db.StringField()
    emergencyContactNumber = db.StringField()
    age = db.IntField()
    applicantdateofbirth = db.DateField()
    physicalExamExpirationDate = db.DateField()

    # applicantlastyearaddressses
    applicantAddresses = db.ListField(db.EmbeddedDocumentField(Address))
    everWorkedForCompany = db.StringField()

    #applicant education history
    applicantSchoolGrade = db.StringField()
    applicantCollegeGrade = db.StringField()
    applicantPostGraduateGrade = db.StringField()

    #employmentHistory
    employmentHistory = db.ListField(db.EmbeddedDocumentField(EmploymentHistory))

    # ExperienceHistory
    employmentExperienceHistory = db.ListField(db.EmbeddedDocumentField(Experience))
    lastFiveYearStatesOperate = db.StringField()
    Listspecialcourses = db.StringField()
    ListanySafeDrivingAwards = db.StringField()

    #AccidentHistory
    employmentAccidentsHistory = db.ListField(db.EmbeddedDocumentField(Accident))

    #violations
    violations = db.ListField(db.EmbeddedDocumentField(TrafficViolations))

    #licences
    licences = db.ListField(db.EmbeddedDocumentField(Licence))

    deniedLicences = db.StringField()
    permitLicences = db.StringField()
    reasonforUnableToPerformActions = db.StringField()
    convictedofafelony = db.StringField()
    answerToAnyQuestion = db.StringField()

    #references
    references = db.ListField(db.EmbeddedDocumentField(Reference))

    #signed By Application
    signature = db.StringField()
    dateOfApplication = db.DateField()
    remarks = db.StringField()

    #drugAndAlcoholTesting
    alcoholTestExecutionDate = db.DateField()
    alcoholTestEmployeeFirstName = db.StringField()
    alcoholTestEmployeeLastName = db.StringField()
    alcoholTestEmployeeSignature = db.StringField()
    alcoholTestSecurityNumber = db.StringField()

    #EmployeeForm7
    employeePrintedName = db.StringField()
    employeeSSNNumber = db.StringField()
    employeeSignature = db.StringField()
    employeeDate = db.DateField()

    #IA Data
    newEmployeerName = db.StringField()
    newEmployeerAddress = db.StringField()
    newEmployeerCity = db.StringField()
    newEmployeerState = db.StringField()
    newEmployeerpostalCode = db.StringField()
    newEmployeerphone = db.StringField()
    newEmployeerFax = db.StringField() # newEmployeerphone => changed => newEmployeerFax
    newEmployeedesignatedEmployeeReprsentative = db.StringField()

    # Ib Data
    prevEmployeerName = db.StringField()
    prevEmployeerAddress = db.StringField()
    prevEmployeerCity = db.StringField()
    prevEmployeerState = db.StringField()
    prevEmployeerpostalCode = db.StringField()
    prevEmployeerphone = db.StringField()
    prevEmployeerFax = db.StringField()# prevEmployeerphone => changed => prevEmployeerFax
    prevEmployeedesignatedEmployeeReprsentative = db.StringField()

    #results
    employeeAlcoholTestRateHigher = db.StringField()
    employeeverifiedDrugTest = db.StringField()
    employeerefuseTest = db.StringField()
    employeeotherViolations = db.StringField()
    prevEmployeeReportDrug = db.StringField()
    answeredYes = db.StringField()

    #IIB
    nameOfPersonProvidingInformation = db.StringField()
    nameOfPersonProvidingInformationTitle = db.StringField()
    nameOfPersonProvidingInformationPhone = db.StringField()
    nameOfPersonProvidingInformationDate = db.DateField()

    # extra form data
    united_state_citizen = db.StringField() # chkbox
    non_united_state_citizen = db.StringField() # chkbox
    lawful_permanent_resident = db.StringField() # chkbox
    alien_registration_number = db.StringField()
    alien_authorized = db.StringField() # chkbox
    expiration_date = db.DateField()
    formi94_reg_number = db.StringField()
    foreign_passport_number = db.StringField()
    issuance_country = db.StringField()

    #editable
    isEditable = db.StringField()


    def to_json(self):
        return {"data": self}

##################################### End Models ########################################################

######################################Start Functions #######################################################

driverForm = model_form(DriversData)

def image_file_path_to_base64_string(filepath: str) -> str:
  with open(filepath, 'rb') as f:
    return base64.b64encode(f.read()).decode()

def split_words(word):
    return [char for char in word]

def string_to_date(record_string):
    dt = None
    try:
        dt = datetime.strptime(record_string, "%Y-%m-%d")
    except:
        try:
            dt = datetime.strptime(record_string, "%Y-%m-%d")
        except:
            dt = "Invalid Date Format"
        dt = "Invalid Date Format"
    return dt

def form_i9_data(user):
    expireson = "2021-03-13"
    img_string = image_file_path_to_base64_string('./templates/img/logo.gif')
    stop_img_string = image_file_path_to_base64_string('./templates/img/stop.png')
    last_name = user.last_name
    first_name = user.first_name
    middle = user.last_name
    address = user.address
    city = user.city
    state = user.state
    zip_code = user.zipCode
    fromDateAddress = user.fromDateAddress
    currentNumberOfYearsAtAddress = ''
    if fromDateAddress:
        currentNumberOfYearsAtAddress = str(int(datetime.now().year) - int(fromDateAddress.year))

    apt_number = "None"
    dateofBirth = user.dateofBirth
    s = split_words(str(user.socialSecurity))
    phone_number = user.phone_number
    email = user.email
    signature = user.signature
    united_state_citizen = user.united_state_citizen
    non_united_state_citizen = user.non_united_state_citizen
    lawful_permanent_resident = user.non_united_state_citizen
    expiration_date = user.expiration_date
    alien_authorized = user.alien_authorized
    applicationApplyAsPosition = user.applicationApplyAsPosition
    companyName = user.companyName
    companyAddress = user.companyAddress
    companyCity = user.companyCity
    companyState = user.companyState
    companyPostCode = user.companyPostCode
    startTime = user.startTime
    addresses = None
    if len(user.addresses) > 0:
        addresses = user.addresses[:3]
    licences = None
    if len(user.licences) > 0:
        licences = user.licences[:3]
        for li in licences:
            li.licenceExpirationDate = str(li.licenceExpirationDate.strftime("%m/%d/%Y"))
    accidents = None
    if len(user.employmentAccidentsHistory) > 0:
        accidents = user.employmentAccidentsHistory[:3]
        for li in accidents:
            li.dateOfAccident = str(li.dateOfAccident.strftime("%m/%d/%Y"))
    alien_registration_number = user.alien_registration_number
    formi94_reg_number = user.formi94_reg_number
    foreign_passport_number = user.foreign_passport_number
    issuance_country = user.issuance_country
    if user.alien_registration_number:
        formi94_reg_number = ''
        foreign_passport_number = ''
        issuance_country = ''
    elif user.formi94_reg_number:
        alien_registration_number = ''
        foreign_passport_number = ''
        issuance_country = ''
    elif user.foreign_passport_number:
        alien_registration_number = ''
        formi94_reg_number = ''
        issuance_country = ''
    elif user.issuance_country:
        alien_registration_number = ''
        formi94_reg_number = ''
        foreign_passport_number = ''

    data = {
        "expireson": expireson,
        "img_string": img_string,
        "stop_img_string": stop_img_string,
        "last_name": last_name,
        "first_name": first_name,
        "middle": middle,
        "address": address,
        "city": city,
        "state": state,
        "currentNumberOfYearsAtAddress": currentNumberOfYearsAtAddress,
        "zip_code": zip_code,
        "dateofBirth": dateofBirth,
        "apt_number": apt_number,
        "social_security":str(user.socialSecurity),
        "social_security1": s[0] if len(s) > 8  else '',
        "social_security2": s[1] if len(s) > 8  else '',
        "social_security3": s[2] if len(s) > 8  else '',
        "social_security4": s[3] if len(s) > 8  else '',
        "social_security5": s[4] if len(s) > 8  else '',
        "social_security6": s[5] if len(s) > 8  else '',
        "social_security7": s[6] if len(s) > 8  else '',
        "social_security8": s[7] if len(s) > 8  else '',
        "social_security9": s[8] if len(s) > 8  else '',
        "email": email,
        "phone_number": phone_number,
        "todayDate": str(datetime.now().strftime("%m/%d/%Y")),
        "signature": signature,
        "dateOfApplication": str(user.dateOfApplication),
        "applicationApplyAsPosition": applicationApplyAsPosition,
        'companyName': companyName,
        'companyAddress': companyAddress,
        'companyCity': companyCity,
        'companyState': companyState,
        'companyPostCode': companyPostCode,
        "startTime": startTime,
        'addresses': addresses,
        'licences': licences,
        'accidents': accidents,
        "page_no": "Page 1 of 3",
        'additional_data': {
            "united_state_citizen": united_state_citizen,
            "non_united_state_citizen": non_united_state_citizen,
            "lawful_permanent_resident": lawful_permanent_resident,
            "alien_authorized": alien_authorized,
            "alien_registration_number": alien_registration_number,
            "expiration_date": expiration_date,
            "formi94_reg_number": formi94_reg_number,
            "foreign_passport_number": foreign_passport_number,
            "issuance_country": issuance_country
        },
        'formi9': True,
        'driver_employ': True,
    }
    return data

######################################End Functions #######################################################

######################################Start Api's #######################################################

@app.route("/", defaults={"path": ""})
@app.route("/<string:path>")
@app.route("/<path:path>")
def index(path):
  print (path)
  return send_from_directory(app.static_folder, "index.html")

@app.route("/admin/", defaults={"path": ""})
@app.route("/admin/<string:path>")
@app.route("/admin/<path:path>")
def index1(path):
  print (path)
  return send_from_directory(app.static_folder, "index.html")

@app.route('/api/files/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if not os.path.isdir("files_upload"):
        os.mkdir("files_upload")
    upload_folder = "./files_upload"
    record = dict(request.form)
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return jsonify({'error': 'Incorrect UserName and Data not found'})
    target = os.path.join(upload_folder, user.user_name)
    if not os.path.isdir(target):
        os.mkdir(target)
    resume = None
    dodMedicalCardFile = None
    dmvFile = None
    driverLicenceFile = None
    if 'resume' in record:
        resume = record['resume']
    if 'dodMedicalCardFile' in record:
        dodMedicalCardFile = record['dodMedicalCardFile']
    if 'dmvFile' in record:
        dmvFile = record['dmvFile']
    if 'driverLicenceFile' in record:
        driverLicenceFile = record['driverLicenceFile']

    if resume:
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        user.update(resume= filename)
        return jsonify({"message": "Successfully Uploded Resume", "status": "true"})
    if dodMedicalCardFile:
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        user.update(dodMedicalCardFile= filename)
        return jsonify({"message": "Successfully Uploaded dodMedicalCardFile", "status": "true" })

    if dmvFile:
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        user.update(dmvFile= filename)
        return jsonify({"message": "Successfully Uploded DVM File", "status": "true"})

    if driverLicenceFile:
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        file.save(destination)
        user.update(driverLicenceFile= filename)
        return jsonify({"message": "Successfully Uploded driverLicenceFile", "status": "true"})

    return jsonify({'error': 'Invalid Data Provided', "status": "false"})

@app.route('/api/get_resume', methods=['GET'])
@cross_origin()
def get_file():
    upload_folder = "./files_upload"
    resume = request.args.get('resume')
    dmvFile = request.args.get('dmvFile')
    dodMedicalCardFile = request.args.get('dodMedicalCardFile')
    driverLicenceFile = request.args.get('driverLicenceFile')
    user_name = request.args.get('user_name')
    user = DriversData.objects(user_name=user_name).first()
    if not user:
        return jsonify({'error': 'Incorrect UserName and Data not found', "status": "false"})

    if resume:
        if user.resume:
            # print(user.resume)
            user_profile_direc = os.path.join(upload_folder, user_name + "/"+ str(user.resume))
            if user_profile_direc:
                print(user_profile_direc)
                try:
                   return send_file(user_profile_direc, as_attachment=True)
                except:
                   return jsonify({'error': 'No Resume found'})
            else:
                return jsonify({'error': 'No Resume found'})
        else:
            return jsonify({'error': 'No Resume found'})

    if dodMedicalCardFile:
        if user.dodMedicalCardFile:
            user_profile_direc = os.path.join(upload_folder, user_name + "/"+ str(user.dodMedicalCardFile))
            if user_profile_direc:
                try:
                   return send_file(user_profile_direc, as_attachment=True)
                except:
                   return jsonify({'error': 'No dodMedicalCardFile found'})
            else:
                return jsonify({'error': 'No dodMedicalCardFile found'})
        else:
            return jsonify({'error': 'No dodMedicalCardFile found'})

    if driverLicenceFile:
        if user.driverLicenceFile:
            # print(user.resume)
            user_profile_direc = os.path.join(upload_folder, user_name + "/"+ str(user.driverLicenceFile))
            if user_profile_direc:
                try:
                   return send_file(user_profile_direc, as_attachment=True)
                except:
                   return jsonify({'error': 'No driverLicenceFile found'})
            else:
                return jsonify({'error': 'No driverLicenceFile found'})
        else:
            return jsonify({'error': 'No driverLicenceFile found'})

    if dmvFile:
        if user.driverLicenceFile:
            # print(user.resume)
            user_profile_direc = os.path.join(upload_folder, user_name + "/"+ str(user.dmvFile))
            if user_profile_direc:
                try:
                   return send_file(user_profile_direc, as_attachment=True)
                except:
                   return jsonify({'error': 'No dmvFile found'})
            else:
                return jsonify({'error': 'No dmvFile found'})
        else:
            return jsonify({'error': 'No dmvFile found'})

    return jsonify({'error': 'Invalid Data Provided '})

@app.route('/api/delete_file', methods=['GET'])
@cross_origin()
def delete_file():
    upload_folder = "./files_upload"
    resume = request.args.get('resume')
    dmvFile = request.args.get('dmvFile')
    dodMedicalCardFile = request.args.get('dodMedicalCardFile')
    driverLicenceFile = request.args.get('driverLicenceFile')
    user_name = request.args.get('user_name')
    user = DriversData.objects(user_name=user_name).first()
    if not user:
        return jsonify({'error': 'Incorrect UserName and Data not found'})

    if resume:
        if user.resume:
            os.remove(os.path.join(upload_folder, user_name + "/" + str(user.resume)))
            user.update(resume= None)
            return jsonify({'success': 'Successfully Deleted Resume'})
        else:
            return jsonify({'error': 'No Resume found'})

    if dodMedicalCardFile:
        if user.dodMedicalCardFile:
            user_profile_direc = os.path.join(upload_folder, user_name + "/" + str(user.dodMedicalCardFile))
            if user_profile_direc:
                try:
                    return send_file(user_profile_direc, as_attachment=True)
                except:
                    return jsonify({'error': 'No dodMedicalCardFile found'})
            else:
                return jsonify({'error': 'No dodMedicalCardFile found'})
        else:
            return jsonify({'error': 'No dodMedicalCardFile found'})

    if driverLicenceFile:
        if user.driverLicenceFile:
            # print(user.resume)
            user_profile_direc = os.path.join(upload_folder, user_name + "/" + str(user.driverLicenceFile))
            if user_profile_direc:
                try:
                    return send_file(user_profile_direc, as_attachment=True)
                except:
                    return jsonify({'error': 'No driverLicenceFile found'})
            else:
                return jsonify({'error': 'No driverLicenceFile found'})
        else:
            return jsonify({'error': 'No driverLicenceFile found'})

    if dmvFile:
        if user.driverLicenceFile:
            # print(user.resume)
            user_profile_direc = os.path.join(upload_folder, user_name + "/" + str(user.dmvFile))
            if user_profile_direc:
                try:
                    return send_file(user_profile_direc, as_attachment=True)
                except:
                    return jsonify({'error': 'No dmvFile found'})
            else:
                return jsonify({'error': 'No dmvFile found'})
        else:
            return jsonify({'error': 'No dmvFile found'})

    return jsonify({'error': 'Invalid Data Provided '})


#######################End File #########################

@app.route('/api/update_record', methods=['POST'])
@cross_origin()
def update_record():
    record = json.loads(request.data)
    if 'physicalExamExpirationDate' in record:
        record["physicalExamExpirationDate"] = string_to_date(record["physicalExamExpirationDate"])
    if 'employmentHistoryfrom' in record:
        record["employmentHistoryfrom"] = string_to_date(record["employmentHistoryfrom"])
    if 'employmentHistoryTo' in record:
        record["employmentHistoryTo"] = string_to_date(record["employmentHistoryTo"])
    if 'experienceFromDate' in record:
        record["experienceFromDate"] = string_to_date(record["experienceFromDate"])
    if 'experienceToDate' in record:
        record["experienceToDate"] = string_to_date(record["experienceToDate"])
    if 'dateOfAccident' in record:
        record["dateOfAccident"] = string_to_date(record["dateOfAccident"])
    if 'dateOfViolation' in record:
        record["dateOfViolation"] = string_to_date(record["dateOfViolation"])
    if 'fromDateAddress' in record:
        record["fromDateAddress"] = string_to_date(record["fromDateAddress"])
    if 'lastYearAddressfrom' in record:
        record["lastYearAddressfrom"] = string_to_date(record["lastYearAddressfrom"])
    if 'lastYearAddressTo' in record:
        record["lastYearAddressTo"] = string_to_date(record["lastYearAddressTo"])
    if 'licenceExpirationDate' in record:
        record["licenceExpirationDate"] = string_to_date(record["licenceExpirationDate"])
    if 'applicationApplyDate' in record:
        record["applicationApplyDate"] = string_to_date(record["applicationApplyDate"])
    if 'applicantdateofbirth' in record:
        record["applicantdateofbirth"] = string_to_date(record["applicantdateofbirth"])
    if 'dateOfViolation' in record:
        record["dateOfViolation"] = string_to_date(record["dateOfViolation"])
    if 'alcoholTestExecutionDate' in record:
        record["alcoholTestExecutionDate"] = string_to_date(record["alcoholTestExecutionDate"])
    if 'employeeDate' in record:
        record["employeeDate"] = string_to_date(record["employeeDate"])
    if 'nameOfPersonProvidingInformationDate' in record:
        record['nameOfPersonProvidingInformationDate'] = string_to_date(record['nameOfPersonProvidingInformationDate'])
    if 'dateofBirth' in record:
        record['dateofBirth'] = string_to_date(record['dateofBirth'])
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return jsonify({'error': 'Incorrect UserName and Data not found'})
    if user.dateOfApplication == None:
        user.update(dateOfApplication=datetime.now())

    for i in record.keys():
        if i == 'user_name':
            continue
        if i == 'addresses':
            user.addresses.clear()
            for k in range(len(record[i])):
                a = Address()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.addresses.append(a)

        if i == 'violations':
            user.violations.clear()
            for k in range(len(record[i])):
                a = TrafficViolations()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.violations.append(a)

        if i == 'employmentAccidentsHistory':
            user.employmentAccidentsHistory.clear()
            for k in range(len(record[i])):
                a = Accident()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.employmentAccidentsHistory.append(a)

        if i == 'employmentExperienceHistory':
            user.employmentExperienceHistory.clear()
            for k in range(len(record[i])):
                a = Experience()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.employmentExperienceHistory.append(a)

        if i == 'applicantAddresses':
            user.applicantAddresses.clear()
            for k in range(len(record[i])):
                a = Address()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.applicantAddresses.append(a)

        if i == 'employmentHistory':
            user.employmentHistory.clear()
            for k in range(len(record[i])):
                a = EmploymentHistory()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.employmentHistory.append(a)

        if i == 'licences':
            user.licences.clear()
            for k in range(len(record[i])):
                a = Licence()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.licences.append(a)

        if i == 'references':
            user.references.clear()
            for k in range(len(record[i])):
                a = Reference()
                for j in record[i][k]:
                    a.__setattr__(j, record[i][k][j])
                user.references.append(a)

        if i in user._fields:
            if i == 'addresses' or i == 'references' or i == 'licences' or i == 'employmentHistory' or i=='resume' or i == 'applicantAddresses' or i == 'employmentExperienceHistory' or i == 'employmentAccidentsHistory' or i == 'violations':
                continue
            user.__setattr__(i, record[i])
    user.save()
    return jsonify({"message": "Successfully Updated User", "data": user.to_json()})

@app.route('/api/delete_record', methods=['POST'])
@cross_origin()
def delete_record():
    record = json.loads(request.data)
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return jsonify({'error': 'user not found'})
    else:
        user.delete()
    return jsonify({"message":"Delete User "+record['user_name']+"Successfully"})

@app.route('/api/register', methods=['PUT'])
@cross_origin()
def register():
    record = json.loads(request.data)
    print(record)
    user = DriversData.objects(user_name=record['user_name']).first()
    if user:
        return jsonify({"error": "user_name already exists"})
    user = DriversData()
    obj = json.loads(request.data)
    for key in obj.keys():
        if key == "password":
            res = str(obj[key]).encode('ascii')
            base64_bytes = base64.b64encode(res)
            base64_string = base64_bytes.decode("ascii")
            user[key] = base64_string
        else:
            user[key] = obj[key]
    user.save()
    return jsonify({"message": "Successfully Registered", "data":user.to_json()})

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    record = json.loads(request.data)
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return json.dumps({'error': 'User Name Not Exists'})
    password = user.password
    password = str(password).encode("ascii")
    sample_string_bytes = base64.b64decode(password)
    password = sample_string_bytes.decode("ascii")
    if record['password'] == password:
        return jsonify(user.to_json())

    return json.dumps({'error': 'Incorect User Name and Password'})


@app.route('/api/get_all_users', methods=['GET'])
@cross_origin()
def get_users():
    users = DriversData.objects().all()
    users_list = []
    if users:
        for user in users:
            users_list.append(user.to_json())
        return jsonify(users_list)
    else:
        return jsonify({'error': 'Unnable to load users'})

#################### Start PDFS HTML###########################

@app.route("/api/html/formi9", methods=['GET'])
@cross_origin()
def form_i9_html():
    u_name = request.args.get('user_name')
    if u_name:
        user = DriversData.objects(user_name=u_name).first()
        if not user:
            return jsonify({'error': 'User Name Not Found'})
        data = form_i9_data(user)
        return render_template("style_css.html", data=data)

@app.route("/api/html/dw4", methods=['GET'])
@cross_origin()
def dw4_html():
    u_name = request.args.get('user_name')
    if u_name:
        user = DriversData.objects(user_name=u_name).first()
        if not user:
            return jsonify({'error': 'User Name Not Found'})
        data = form_i9_data(user)
        data['formi9'] = False
        return render_template("style_css.html", data=data)

#################### Emd PDFS HTML###########################


#################### Start PDF's ###########################

@app.route('/api/pdf/new_employee', methods=['GET'])
@cross_origin()
def new_employeee_pdf():
    u_name = request.args.get('user_name')
    if u_name:
        user = DriversData.objects(user_name=u_name).first()
        if not user:
            return jsonify({'error': 'User Name Not Found'})

        first_name = user.first_name
        last_name = user.last_name
        dateofBirth = user.dateofBirth
        socialSecurity = user.socialSecurity
        address = user.address
        maritial_status = user.maritial_status
        NumberofDependantsUnder17 = user.NumberofDependantsUnder17
        NumberofDependantsOver17 = user.NumberofDependantsOver17
        gender = user.gender

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "dateOfBirth": dateofBirth,
            "maritial_status": maritial_status,
            "social_security": socialSecurity,
            "address": address,
            "NumberofDependantsUnder17": NumberofDependantsUnder17,
            "NumberofDependantsOver17": NumberofDependantsOver17,

        }
        html = render_template("new_employee.html", data=data)
        pdf = pdfkit.from_string(html, False, configuration=PDFKIT_CONFIGURATION )
        # pdf = pdfkit.from_string(html, False)
        resp = make_response(pdf)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment; filename=new_employee '+u_name+'.pdf'

        return resp
    else:
        return json.dumps({"message": "Invalid Data", "code": "201"})

@app.route('/api/pdf/formi9', methods=['GET'])
@cross_origin()
def form_i_9():
    u_name = request.args.get('user_name')
    if u_name:
        user = DriversData.objects(user_name=u_name).first()
        if not user:
            return jsonify({'error': 'User Name Not Found'})
        data = form_i9_data(user)
        options = {
            'page-size': 'A4',
            'encoding': 'utf-8',
            'margin-top': '1.8cm',
            'margin-bottom': '0cm',
            'margin-left': '0.5cm',
            'margin-right': '0.5cm'
        }
        html = render_template("style_css.html", data=data)
        pdf = pdfkit.from_string(html, False, options=options, configuration=PDFKIT_CONFIGURATION)
        resp = make_response(pdf)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment; filename=formi9'+u_name+'.pdf'
        return resp

    else:
        return jsonify({'error': 'Invalid Data'})

@app.route('/api/pdf/dw4', methods=['GET'])
@cross_origin()
def driver_employ():
    u_name = request.args.get('user_name')
    if u_name:
        user = DriversData.objects(user_name=u_name).first()
        if not user:
            return jsonify({'error': 'User Name Not Found'})
        data = form_i9_data(user)
        options = {
            'page-size': 'A4',
            'encoding': 'utf-8',
            'margin-top': '1.8cm',
            'margin-bottom': '0cm',
            'margin-left': '0.5cm',
            'margin-right': '0.5cm'
        }
        data['formi9'] = False
        html = render_template("style_css.html", data=data)
        pdf = pdfkit.from_string(html, False, options=options, configuration=PDFKIT_CONFIGURATION)
        resp = make_response(pdf)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment; filename=driver_employ '+u_name+'.pdf'
        return resp

    else:
        return jsonify({'error': 'Invalid Data'})
####################End PDF's###########################

# @app.route('/')
# @cross_origin()
# def index():
#     return app.send_static_file('index.html')



if __name__ == "__main__":
    app.run(debug=True)
    app.listen(process.env.PORT or 5000, ...)


