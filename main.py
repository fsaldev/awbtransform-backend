import base64
import json
from multiprocessing import process
from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import cross_origin
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import hashlib
import pdfkit

app = Flask(__name__, static_folder='./build', static_url_path='/')
app.config['MONGODB_SETTINGS'] = {
    'db': 'awbTransport1',
    'host': 'mongodb+srv://test:test1234@test.iocw1.mongodb.net/awbTransport1',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
# wkhtmltopdf = Wkhtmltopdf(app)

class EmploymentHistory(db.EmbeddedDocument):
    employmentHistoryfrom = db.DateField()
    employmentHistoryTo = db.DateField()
    employmentHistorystatus = db.StringField()
    employmentHistoryposition = db.StringField()
    employmentHistoryaddress = db.StringField()
    employmentHistorycompanyPhone = db.StringField()
    employmentHistoryreasonForLeaving = db.StringField()
    employmentHistorysubjecttotheFMCSRs = db.BooleanField()
    employmentHistorydrugandalcoholTesting = db.BooleanField()

class Experience(db.EmbeddedDocument):
    experienceclassofEquipment = db.DateField()
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

class DriversData(db.Document):
    user_name = db.StringField()
    password = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    email = db.StringField()
    dateofBirth = db.StringField()
    socialSecurity = db.IntField()
    address = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zipCode = db.StringField()
    lastThreeYearResidenceCheck = db.BooleanField()
    maritial_status = db.StringField()
    NumberofDependantsUnder17 = db.IntField()
    NumberofDependantsOver17 = db.IntField()
    #lastyearaddressses
    addresses = db.ListField(db.EmbeddedDocumentField(Address))

    startTime = db.StringField()
    hearAbout = db.StringField()
    eligibletoWorkInUnitedState = db.BooleanField()
    classAExperienceLevel = db.BooleanField()
    willingForDrugTest = db.BooleanField()
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
    everWorkedForCompany = db.BooleanField()
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

    deniedLicences = db.BooleanField()
    permitLicences = db.BooleanField()
    reasonforUnableToPerformActions = db.BooleanField()
    convictedofafelony = db.BooleanField()
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
    newEmployeerphone = db.StringField()
    newEmployeedesignatedEmployeeReprsentative = db.StringField()

    # Ib Data
    prevEmployeerName = db.StringField()
    prevEmployeerAddress = db.StringField()
    prevEmployeerCity = db.StringField()
    prevEmployeerState = db.StringField()
    prevEmployeerpostalCode = db.StringField()
    prevEmployeerphone = db.StringField()
    prevEmployeerphone = db.StringField()
    prevEmployeedesignatedEmployeeReprsentative = db.StringField()

    #results
    employeeAlcoholTestRateHigher = db.BooleanField()
    employeeverifiedDrugTest = db.BooleanField()
    employeerefuseTest = db.BooleanField()
    employeeotherViolations = db.BooleanField()
    prevEmployeeReportDrug = db.BooleanField()
    answeredYes = db.BooleanField()

    #IIB
    nameOfPersonProvidingInformation = db.StringField()
    nameOfPersonProvidingInformationTitle = db.StringField()
    nameOfPersonProvidingInformationPhone = db.StringField()
    nameOfPersonProvidingInformationDate = db.DateField()

    def to_json(self):
        return {"data": self}


driverForm = model_form(DriversData)

@app.route('/api/update_record_form1', methods=['POST'])
@cross_origin()
def update_record():
    record = json.loads(request.data)
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return jsonify({'error': 'data not found'})

    user.update(first_name=record['first_name'])
    user = DriversData.objects(user_name=record['user_name']).first()
    return jsonify(user.to_json())

@app.route('/api/delete_record', methods=['DELETE'])
@cross_origin()
def delete_record():
    record = json.loads(request.data)
    user = DriversData.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())

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
            result = hashlib.sha3_256(str(obj[key]).encode())
            user[key] = result.hexdigest()
        else:
            user[key] = obj[key]
    user.save()
    return jsonify({"data": user.to_json()})

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    record = json.loads(request.data)
    user = DriversData.objects(user_name=record['user_name']).first()
    if not user:
        return jsonify({'error': 'User Name Not Exists'})

    return jsonify(user.to_json())

@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@app.route('/api/pdf/new_employee', methods=['GET'])
@cross_origin()
def new_employeee_pdf():
    u_name = request.args.get("user_name")
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
        pdf = pdfkit.from_string(html, False )
        resp = make_response(pdf)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment; filename=new_employee '+u_name+'.pdf'

        return resp
    else:
        return json.dumps({"message": "Invalid Data", "code": "201"})

def image_file_path_to_base64_string(filepath: str) -> str:
  with open(filepath, 'rb') as f:
    return base64.b64encode(f.read()).decode()

@app.route('/api/pdf/formi9', methods=['GET'])
@cross_origin()
def form_i_9():
    data = {
    "expireon": "never",
    "img_string": image_file_path_to_base64_string('./templates/img/logo.gif')
    }
    html = render_template("form19.html", data=data)
    options = {
        'page-size': 'A4',
        'encoding': 'utf-8',
        'margin-top': '0cm',
        'margin-bottom': '0cm',
        'margin-left': '0cm',
        'margin-right': '0cm'
    }
    pdf = pdfkit.from_string(html, False ,options=options)
    resp = make_response(pdf)
    resp.headers['Content-Type'] = 'application/pdf'
    resp.headers['Content-Disposition'] = 'attachment; filename=form19.pdf'

    return resp
if __name__ == "__main__":
    app.run(debug=True)
    app.listen(process.env.PORT or 5000, ...)


