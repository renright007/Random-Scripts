
# Import Packages
from os import name
from signal import signal
from simple_salesforce import Salesforce, SalesforceLogin, SFType
import json
import requests

# Data from Otter Sign-Up
sign_up_data = {
    "Client ID":"TOheAydvF6Q",
    "Client Name":"John Doe",
    "Email":"johndoe@abc.ca",
    "Business Name":"ABC LTD",
    "Number of Locations":7,
    "Phone Number":"778-123-4577",
    "Role":"Operations Analyst"
    }

# Salesforce Login Info
username = 'username'
password = 'password'
security_token = 'security_token'
domain = 'login'

# Define Salesforce SessionID and Instanace
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token)
sf = Salesforce(instance_url=instance, session_id=session_id)

# Define the Object APIs we are looking to connect to
accounts = SFType('Account', session_id, instance)
contacts = SFType('Contact', session_id, instance)

# Create our business detail dictionary including the SF field APIs on the left
business_data = {
    'Name': sign_up_data["Business Name"],
    'Number_of_locations__c': sign_up_data["Number of Locations"]
    }

# Check to see if the business name already exists
if sign_up_data['Business Name'] not in accounts:

    # Create our new account
    response_account = accounts.create(business_data)
    accountId = response_account.get('id')  # Extract our ID

    # Likewise, define our client information and SF API fields
    contact_data = {
        'LastName': sign_up_data["Client Name"].split(" ")[-1],
        'FirstName': " ".join(sign_up_data["Client Name"].split(" ")[:-1]),
        'CustomerAccount': accountId,
        'PhoneNumber': sign_up_data["Phone Number"],
        'Email': sign_up_data["Email"],
        'Title': sign_up_data["Role"],
        'Referral Source': 'Direct Sign Up'
        }

    # Create our new contact
    response_contact = contacts.create(contact_data)
    contactId = response_contact.get('id')  # Extract our new contact ID

    print('Record Created')
    print('-'.center(50,('-')))
    print('Account Id: {0}'.format(accountId))
    print('Contact Id: {0}'.format(contactId))

else:
    print('Client already exists')
