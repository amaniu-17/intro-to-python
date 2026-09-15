


#importing libraries
import json
import os
from faker import Faker
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet

#lodad or create a persistant encryption key
KEY_FILE = "encription.key"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        encription_key = f.read()
else:
    encription_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(encription_key)

#initialize the faker engine and anonymizer engine
fake = Faker()
anonymizer = Anonymizer(encryption_key=encription_key)

#prompt user for data length
length = int(input("Enter the desired number of synthetic patient datasets you would like"))

#initialize data variable
data = []

#call faker_len function to generate names
for _ in range(length):
    data.append(fake.profile())

#print data to termial
print("unencrypted data: ", data)
print(data)

#turn data into a string
data_str = json.dumps(data, default=str)

#run anonymizer
secure_data = anonymizer.encrypt_text(data_str)

#show encrypted data to user
print ("encrypted data: ")
print(secure_data)

#create boolean question function for file write
def write_to_file_question(question:str) -> bool:
    while True:
        write_decision = input(f"{question} (y/n): ").strip().lower()
        if write_decision in ("y", "yes"):
            return True
        if write_decision in ("n", "no"):
            return False

        print("Invalid input. Please enter 'y' or 'n'.")

#ask if they would like to write data to file
write_bool = write_to_file_question("Would you like to write this data to file?")

#write data if/else logic
if write_bool == True:
    custom_name = input("Enter the name for the file. (no special characters): ")

    file_name = (f"{custom_name}.txt")

    with open(file_name, "w", encoding = "utf-8") as file_name:
        file.write(secure_data)

    print(f"Saved tp {file_name}")
else:
    print ("Data not saved. All data will be lost when application is closed")














