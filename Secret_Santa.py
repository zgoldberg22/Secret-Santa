import smtplib
import random
import re

# Person class to store info for name, email and name of person they are giving to
class Person:
  name = ""
  email = ""
  giving_to = ""

  def __init__(self, name="", email=""):
    self.name = name
    self.email = email
  
  #method used for testing
  def print_info(self):
    print(self.name, ": ", self.email)

#returns true if email is valid, returns false if invalid email
  #valid if string is in correct format of email, does not show if the email actually exists 
def check_email(email):
  regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

  if(regex.match(email)):
    return True
  else:
    return False

#function to randomly assign who a person is giving to, while making sure no one is assigned themselves
  #parameter is a list of Person objects
def assign_santas(people_list):
  shuffled_list = people_list.copy()
  notAllDiff = True
  while(notAllDiff):
    random.shuffle(shuffled_list)
    for x in range(len(people_list)):
      if people_list[x].name == shuffled_list[x].name:
        notAllDiff = True
        break 
      else:
        notAllDiff = False
  
  #assign giving_to in person object list
  for x in range(len(people_list)):
    people_list[x].giving_to = shuffled_list[x].name.upper()

#Sends emails using smtp library
def send_emails(from_email, password, people_list):
  server = smtplib.SMTP_SSL("smtp.gmail.com")
  server.login(from_email, password)

  subject = "SECRET SANTA"
  for person in people_list:
    text = person.name + ", \n\nYou are giving to " + person.giving_to + ".\n\nGood luck!"

    msg = 'Subject: {}\n\n{}'.format(subject, text)

    server.sendmail(from_email, person.email, msg)

  server.quit()


#main code to get input and generate secret santas
if __name__ == "__main__":
  #input sender's email and password
  print("SECRET SANTA GENERATOR")
  print("Directions:\n1. Input each person participating in the secret santa with their name and their valid email address in the following format (make sure to use a colon to separate):\n\tName:email@ex.com\n2. Once you are done inputting names, type: stop")

  people = [] #holds Person objects

  #ask for user input to get names and emails
  name_input = input("\nEnter name:email >> ")
  while True:
    if len(people) <= 1 and name_input.lower() == "stop":
      print("There needs to be more than 1 person inputted. Please enter more people.")
    elif name_input.lower() == "stop":
      break
    elif ':' in name_input:
      info = name_input.split(':')
      if check_email(info[1]):
        people.append(Person(info[0].title(), info[1].strip()))
      else:
        print("Invalid email. Please re-enter person and email")
    else:
      print("Invalid input. Please enter again")

    name_input = input("Enter name:email >> ")

  #randomly assigning people secret santas
  assign_santas(people)
  print("\nSecret Santas have been assigned.\n")

  #smtp needs email information about who the email is coming from
  print("\nEnter an email and password for 'from' email: ")

  #ensures email is in valid format
  while True:
    sender_email = input('Enter "from" Email >> ')
    if check_email(sender_email):
      break
    else:
      print("Invalid email. Please re-enter email")

  sender_password = input('Enter "from" Email Password >> ')

  send_emails(sender_email, sender_password, people)
  print("\nMessages have been sent.")