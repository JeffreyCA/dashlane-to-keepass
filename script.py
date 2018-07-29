import argparse
import csv
import os.path
import traceback
import validators
import xml.etree.ElementTree as ET

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class PWEntry:
    def __init__(self, title, url, username, email, password, note):
        self.title = title
        self.url = url
        self.username = username
        self.email = email
        self.password = password
        self.note = note

def isAmbiguous(text):
    return "\"" in text

def isValidSite(text):
    return validators.domain(text) or validators.ip_address.ipv4(text) or validators.ip_address.ipv6(text)

def readCsv(filename, verbose = False):
    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, quotechar='"', delimiter=',', doublequote=False)
        ambiguousEntries = []
        entries = []
        processed = 0

        for row in reader:
            try:
                if len(row) >= 5:

                    name = row[0]
                    site = row[1]
                    user = row[2]
                    email = row[3] if row[4] else ""
                    password = row[4] if email else row[3]
                    note = row[5] if (len(row) > 5 and row[5]) else ""

                    if isAmbiguous(note):
                        note = note.replace('"', '')

                    entry = PWEntry(name, site, user, email, password, note)

                    if isAmbiguous(email) or isAmbiguous(password) or (len(row) > 5 and isAmbiguous(note)):
                        if verbose:
                            print("Skipped: " + site)
                        ambiguousEntries.append(entry)
                        continue

                    if isValidSite(site):
                        processed += 1
                        entries.append(PWEntry(name, site, user, email, password, note))
                    elif verbose:
                        print("Skipped: " + str(row))

            except:
                print(traceback.format_exc())

        return entries, ambiguousEntries

def writeEntries(filename, entries, groupName = "General", verbose = False):
    processed = 0
    pwlist = ET.Element("pwlist")

    for entry in entries:
        processed += 1
        pwentry = ET.SubElement(pwlist, "pwentry")

        ET.SubElement(pwentry, "group").text = groupName
        ET.SubElement(pwentry, "title").text = entry.title
        ET.SubElement(pwentry, "username").text = entry.username
        ET.SubElement(pwentry, "url").text = entry.url
        ET.SubElement(pwentry, "password").text = entry.password

        note = ""

        if entry.email:
            note += "email: " + entry.email

        if entry.note:
            # Append note after above email
            if note:
                note += "\n"
            note += entry.note
        
        if note:
            ET.SubElement(pwentry, "notes").text = note

        if verbose:
            print("Processing " + entry.url)

    tree = ET.ElementTree(pwlist)
    indent(pwlist)

    tree.write(filename, encoding="UTF-8", xml_declaration=True)
    
    if verbose:
        print("")
    print("Successfully converted " + str(processed) + " password entries.")

def outputAmbiguousEntries(ambiguousEntries):
    if ambiguousEntries:
        print("The following password entries were found to be ambiguous due to double quotation marks (\") in its fields.")
        print("Please manually add the passwords for these sites:\n")

        for entry in ambiguousEntries:
            print(entry.url)
        print("")

def indent(elem, level = 0):
    """https://stackoverflow.com/a/33956544"""
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
    parser = argparse.ArgumentParser(description='Converts Dashlane-exported CSV files to KeePass XML format. Supports password entries with both username and email fields.')
    parser.add_argument('csv_file', metavar='input_csv', type=str,
                        help='Dashlane-exported CSV input file')

    parser.add_argument('xml_file', metavar='output_xml', type=str,
                        help='KeePass XML output file')

    parser.add_argument('-g', '--group', type=str, default="General",
                        help='name of group the passwords are stored under (by default the group is \'General\')')

    parser.add_argument('-v', '--verbose', action="store_true",
                        help='enable verbose logging')

    args = parser.parse_args()

    csv_file = args.csv_file
    xml_file = args.xml_file
    group = args.group
    verbose = args.verbose

    if not os.path.exists(csv_file):
        print("Input file " + csv_file + " does not exist!")
        return

    entries, ambiguousEntries = readCsv(csv_file, verbose)

    outputAmbiguousEntries(ambiguousEntries)
    writeEntries(xml_file, entries, group, verbose)
    
main()
