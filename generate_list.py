import hashlib

STARTNUMBER = 21422000
COUNT = 100
SALT = "Test123"

for ticket_number in range(STARTNUMBER, STARTNUMBER + COUNT):
    print "Ticket number: " + str(ticket_number)
    ticket_checksum = int(hashlib.sha1(SALT + str(ticket_number)).hexdigest(), 16)
    ticket_checksum = int(str(ticket_checksum)[:5])
    print "Ticket Checksum: " + str(ticket_checksum)
    registration_number = int(str(ticket_number) + str(ticket_checksum))
    print "==> Registration Number: " + str(registration_number)
