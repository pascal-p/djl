import uuid
from profiles.models import Profile
from customers.models import Customer

def generate_code():
    return str(uuid.uuid4()).replace('-', '')[:12].upper()

def get_salesman_from_id(id):
    return Profile.objects.get(id=id).user.username

def get_customer_from_id(id):
    return Customer.objects.get(id=id)
