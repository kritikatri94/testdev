from myapp.models import Member


def check_unique_name(id, firstname, lastname):
    member = Member.objects.filter(firstname=firstname,lastname=lastname)
    if member.exists():
        if member.first().id == int(id):
            return True
        return False
    return True
