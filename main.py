from datetime import datetime

print("🔰 Welcome to AutoComplaint - Smart Legal Complaint Generator")
print("-" * 60)

# Get user input
name = input("👤 Your Full Name: ")
address = input("🏠 Your Address: ")
city = input("🏙️  City: ")
against_whom = input("👮 Who are you complaining against (person/organization)? ")
incident_description = input("📝 Describe the issue in detail: ")
incident_dates = input("📅 Date(s) of Incident (e.g., 01-04-2025 to 10-04-2025): ")
location = input("📍 Location of the Incident: ")
contact = input("📞 Your Contact Number: ")

# Get current date
today = datetime.now().strftime("%d-%m-%Y")

# Generate complaint
complaint = f"""
📄 Generated Legal Complaint:

To,  
The Officer in Charge,  
{city} Police Station  

Subject: Formal Legal Complaint Against {against_whom}  

Respected Sir/Madam,

I, {name}, residing at {address}, {city}, wish to lodge a formal complaint against {against_whom} for the following serious concern:

❗ **Nature of Complaint**  
{incident_description}

📆 **Date & Time of Incident:**  
{incident_dates}

📍 **Location:**  
{location}

📝 **Request for Action**  
I kindly request your office to take immediate and appropriate legal action against the responsible individuals/organization. I am willing to cooperate with further investigation if required.

Attached are my identification documents and supporting evidence.

Thanking you,  
Sincerely,  
{name}  
📅 Date: {today}  
📞 Contact: {contact}
"""

print(complaint)
