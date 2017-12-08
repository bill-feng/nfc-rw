import nfc
import ndef
import pprint

END = '\033[0m'
RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

def startup(targets):
    """ Device ready, waiting for tag. """
    print YELLOW + "Waiting to read NFC tag...\n" + END
    return targets

def dump(tag):
    print "Dumping tag content:"
    print BLUE + str("\n".join(["  " + line for line in tag.dump()])) + "\n" + END

def identify(tag):
    print "Tag type: " + BLUE + str(tag.ndef) + "\n" + END

def format(tag):
    tag.format(None, 0)
    print BLUE + "Tag formatted." + "\n" + END

def read(tag):
    # Read & print records
    print "Current Records:" + BLUE
    if len(tag.ndef.records) > 0:
        for record in tag.ndef.records:
            print record
    else:
        print "None."
    print END

def write(tag):
    # Write records
    try:
        tag.ndef.records = [ndef.TextRecord('Hello World')]
        print GREEN + "Write success!\n" + END
        # Print new records
        print "New Records:" + BLUE
        for record in tag.ndef.records:
            print record
        print END
    except nfc.tag.TagCommandError as err:
        print RED + "Write to tag failed: " + str(err) + END

def standby(tag):
    # Choose action
    print YELLOW + "d) Dump e) Eject f) Format i) Identify r) Read w) Write " + END
    key = raw_input("Action: ")
    print ""
    # Execute action
    if key == 'd':
        dump(tag)
    elif key == 'e':
        print GREEN + "Tag ejected. You can safely remove the tag.\n" + END
        return True
    elif key == 'f':
        format(tag)
    elif key == 'i':
        identify(tag)
    elif key == 'r':
        read(tag)
    elif key == 'w':
        write(tag)
    else:
        print RED + "Invalid input.\n" + END
    return False

def engaged(tag):
    """ Tag is engated, identify tag. """
    print GREEN + str(tag) + " engaged.\n" + END
    done = False
    while not done:
        done = standby(tag)
    return True

def released(tag):
    """ Tag is released. """
    print "Tag released. "
    print YELLOW + "Waiting to read NFC tag...\n" + END


device = nfc.ContactlessFrontend('usb')
print ""
print GREEN + "Connected to " + str(device) + "\n" + END
if device:
    while device.connect(rdwr={
        'on-startup': startup,
        'on-connect': engaged,
        'on-release': released,
    }):
        pass

print RED + "\n\nDevice disconnected.\n" + END