from collegegatepass.models import PassRequestModel, StudentModel


def getadminpassrequests():

    passrequests = []

    for passrequest in PassRequestModel.objects.all():

        student = StudentModel.objects.filter(rno=passrequest.studentid).first()

        if student is not None:
            img = str(student.photo).split("/")[1]
            passrequest.photo = img

            passrequest.rno = student.rno
            passrequest.name = student.name
            passrequest.branch = student.branch
            passrequest.year = student.year
            passrequest.section = student.section

            passrequests.append(passrequest)

    return passrequests


def getdepartmentpassrequests(branch):

    passrequests = []

    for passrequest in PassRequestModel.objects.all():

        student = StudentModel.objects.filter(rno=passrequest.studentid).first()

        if student is not None:

            if student.branch==branch:

                img = str(student.photo).split("/")[1]
                passrequest.photo = img

                passrequest.rno = student.rno
                passrequest.name = student.name
                passrequest.branch = student.branch
                passrequest.year = student.year
                passrequest.section = student.section

                passrequests.append(passrequest)

    return passrequests

def getstudentpassrequests(rno):

    passrequests = []

    for passrequest in PassRequestModel.objects.filter(studentid=rno):

        student = StudentModel.objects.filter(rno=rno).first()

        if student is not None:

            img = str(student.photo).split("/")[1]
            passrequest.photo = img

            passrequest.rno = student.rno
            passrequest.name = student.name
            passrequest.branch = student.branch
            passrequest.year = student.year
            passrequest.section = student.section

            passrequests.append(passrequest)

    return passrequests
