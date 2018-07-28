import csv
import traceback
import validators
import xml.etree.ElementTree as ET

class PWEntry:
	def __init__(self, title, url, username, email, password, note):
		self.title = title
		self.url = url
		self.username = username
		self.email = email
		self.password = password
		self.note = note

def readCsv(filename):
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		entries = []
		processed = 0

		for row in reader:
			try:
				if len(row) >= 5:
					name = row[0]
					site = row[1]
					user = row[2]
					email = row[3] if row[4] else ""
					pw = row[4] if email else row[3]
					note = row[5] if (len(row) > 5 and row[5]) else ""

					if validators.domain(site) or validators.ip_address.ipv4(site) or validators.ip_address.ipv6(site):
						processed += 1
						entries.append(PWEntry(name, site, user, email, pw, note))
			except:
				print(traceback.format_exc())

		return entries

def writeEntries(filename, entries, groupName = "General"):
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
		ET.SubElement(pwentry, "notes").text = entry.note

		print("Processing " + entry.url)

	tree = ET.ElementTree(pwlist)
	indent(pwlist)

	tree.write(filename, encoding="UTF-8", xml_declaration=True)
	print("\nSuccessfully converted " + str(processed) + " entries.")

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

entries = readCsv('file.csv')
writeEntries("entries.xml", entries, "Custom Group Name")
