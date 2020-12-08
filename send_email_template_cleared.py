import os,sys
import csv
import base64
from sendgrid.helpers.mail import *
from sendgrid import SendGridAPIClient


# if os.name == 'nt':
#     print("Windows OS Detected. Adding API Key")
#     os.system("setx SENDGRID_API_KEY {0}".format(adminPhiAPIKey))
# elif os.name == 'posix':
#     print("Mac OS Detected. Adding API Key")
#     os.system("export SENDGRID_API_KEY="+adminPhiAPIKey)

# from address we pass to our Mail object, edit with your name
FROM_EMAIL = '################'
error_count = 0

# update to your dynamic template id from the UI
TEMPLATE_ID = '###################'  

def SendDynamic(TO_EMAIL):
    # create Mail object and populate
    global error_count
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL)
    message.template_id = TEMPLATE_ID

    # Attachment 1
    file_path = "##############.pdf"
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment1 = Attachment()
    attachment1.file_content = FileContent(encoded)
    attachment1.file_type = FileType('application/pdf')
    attachment1.file_name = FileName('#############.pdf')
    attachment1.disposition = Disposition('attachment')
    message.attachment = attachment1

    # Attachment 2
    file_path = "#################.pdf"
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment2 = Attachment()
    attachment2.file_content = FileContent(encoded)
    attachment2.file_type = FileType('application/pdf')
    attachment2.file_name = FileName('###############.pdf')
    attachment2.disposition = Disposition('attachment')
    message.attachment = attachment2
    
    
    # create our sendgrid client object, pass it our key, then send and return our response objects
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Response code: ",response.status_code)
        if response.status_code==202:
            error_count=0
        print("Email SENT!")
    except Exception as e:
        error_count+=1
        print("Error: {0}\nERROR COUNT --> {1}".format(e,error_count))
        with open("unsuccessful.txt", "a") as fu:
            fu.write(TO_EMAIL+"\n")
        fu.close()
    return response.status_code
if __name__ == "__main__":
    with open('emails.csv', 'r') as emails:
        count = 1
        for TO_EMAIL in emails:
            mail=str(TO_EMAIL).rstrip()
            print("\n\n"+str(count) + ': ', mail)
            try:
                resp=SendDynamic(mail)
            except KeyboardInterrupt:
                break
            except:
                print("############### EXCEPTION OUTSIDE ############### --------------- HERE ----------->")
                if error_count >= 5:
                    os.system(
                        "say 'DAILY LIMIT HIT! Please clear the last 5 entries from unsuccessful.txt'")
                    sys.exit(
                "\n\nDAILY LIMIT HIT! Please clear the last 5 entries from \"unsuccessful.txt\"\n\n")
            count = count + 1
