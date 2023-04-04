### Generate CA "our CA here will be our faculty since we can't really go and ask the approval of the certif of a real CA, so our faculty will be the truseted partie"

1. Generate RSA

openssl genrsa -aes256 -out FI_USTHB-key.pem 4096
####
####
####

2. Generate a public CA Cert
     
openssl req -new -x509 -sha256 -days 365 -key FI_USTHB-key.pem -out FI_USTHB.pem
passphrase was usthb2023 for our case 
####
####
####

### Optional Stage: View Certicate's Content

openssl x509 -in FI_USTHB.pem -text
openssl x509 -in FI_USTHB.pem -purpose -noout -text

####
####
####

### Generate Certificate for a user "staff/teacher/student" 
1. Create a RSA key
     
### for the staff member :
openssl genrsa -out SIQ_DEPT-key.pem 4096
### for the professor:
openssl genrsa -out professor-key.pem 4096
### for the student "samy" 
openssl genrsa -out samy-key.pem 4096
### for the student "test" 
openssl genrsa -out test-key.pem 4096

2. Create a Certificate Signing Request (CSR)

### for the staff member
openssl req -new -sha256 -key SIQ_DEPT-key.pem -out SIQ_member.csr -subj "/C=DZ/ST=ALGIERS/O=FI_USTHB/OU=SIQ/CN=SIQ_member /emailAddress=SIQ_member@usthb.com/UID=SIQ_member_UID"
### for the professor 
openssl req -new -sha256 -key professor-key.pem -out Professor_XYZ.csr -subj "/C=DZ/ST=ALGIERS/O=FI_USTHB/OU=SIQ/CN=Professor_XYZ /emailAddress=Professor_XYZ@usthb.com/UID=Professor_UID"
### for the student 
openssl req -new -sha256 -key samy-key.pem -out samy.csr -subj "/C=DZ/ST=ALGIERS/O=FI_USTHB/OU=M1_SSI/CN=ZAKOUR_Amrane_Samy /emailAddress=ZAKOUR_AS@usthb.com/UID=191931069470"
### for the student test
openssl req -new -sha256 -key test-key.pem -out test.csr -subj "/C=DZ/ST=ALGIERS/O=FI_USTHB/OU=M1_SSI/CN=test /emailAddress=ourhesf@gmail.com/UID=191931069470"


3. Create a `extfile` with all the alternative names " can add other alternative infos than the mail" 
### for the staff member
echo "subjectAltName=email:SIQ_member@gmail.com" >> extfile_staff.cnf
### for the professor 
echo "subjectAltName=email:Professor_XYZ@gmail.com" >> extfile_prof.cnf
### for the student
echo "subjectAltName=email:ourhesf@gmail.com" >> extfile_student.cnf

     
# optional "to add the auth option in the certif" 
echo extendedKeyUsage = serverAuth >> extfile.cnf

4. Create the certificate

### for the staff member
openssl x509 -req -sha256 -days 365 -in SIQ_member.csr -CA FI_USTHB.pem -CAkey FI_USTHB-key.pem -out SIQ_member_cert.pem -extfile extfile_staff.cnf -CAcreateserial
### for the professor 
openssl x509 -req -sha256 -days 365 -in Professor_XYZ.csr -CA FI_USTHB.pem -CAkey FI_USTHB-key.pem -out Professor_XYZ_cert.pem -extfile extfile_prof.cnf -CAcreateserial
### for the student 
openssl x509 -req -sha256 -days 365 -in samy.csr -CA FI_USTHB.pem -CAkey FI_USTHB-key.pem -out samy_cert.pem -extfile extfile_student.cnf -CAcreateserial
### for the student test
openssl x509 -req -sha256 -days 365 -in test.csr -CA FI_USTHB.pem -CAkey FI_USTHB-key.pem -out test_cert.pem -extfile extfile_student.cnf -CAcreateserial


## Verify Certificates 
ex:
openssl verify -CAfile FI_USTHB.pem -verbose samy_cert.pem 


### install the certif on a trusted root ca, On Windows

In Command Prompt, run:

certutil.exe -addstore root C:\ca.pem
certutil.exe is a built-in tool (classic System32 one) and adds a system-wide trust anchor.

### ps we can create a certif chain 
root -> siq then : 
prof or student 