# Script to process the XML output of Adacore gnatmetric command
# and write it to a CSV file. See Input_Sample.xml for the XML
# structure it was developed against.
#
# Last known compatibility: Python 3.8
#
# TODO 
#    - Error handling
#    - Parameterise Input/output files
#
import xml.etree.ElementTree as ET
import csv
import logging

# Reference Values

## Flags
logging.basicConfig( format='%(asctime)s %(message)s', level=logging.INFO ) 

## File names

inputFileName = 'Test.xml' 
outputFilename = 'Test.csv'

## XML tag names in the input file
constFileTag = 'file'
constUnitTag = 'unit'

# function to write CSV file
#
# Input Param: A list of dictionary items
#
def writeCSV( listOfDictDataItems ):

	logging.info( 'Preparing to write %s lines to output CSV - %s', len( listOfDictDataItems ), outputFilename)

	output_fieldnames = [
		'filename',
		'unit',
		'unit_serial_num',
		'kind',
		'cyclomatic_complexity'
	]

	with open( outputFilename, 'w', encoding='utf-8', newline='' ) as csvfile:
		writer = csv.DictWriter( csvfile, fieldnames = output_fieldnames )

		writer.writeheader() #write header
		writer.writerows( listOfDictDataItems )

	logging.info( "Wrote - '%s'", outputFilename)

# Main()

logging.info("Starting (Input file: %s)", inputFileName)
tree = ET.parse(inputFileName)
logging.info('Parsed XML')
root = tree.getroot()
listData = [] # will hold data of interest extracted from the input XML file

# For each <file> under root
for file in root.iter(constFileTag):

	fileName = file.attrib.get('name')
	logging.debug( 'Processing details of file - %s', fileName)

	# set/reset vars we use for each change in file
	sr_num = 0 
	listTempUnitsInThisFile = []

	# for every <unit> under <file> - no matter how deep!
	for unit in file.findall(".//unit"):

		# extract unit details
		unitName = unit.attrib["name"]
		unitKind = unit.attrib["kind"]

		# Look for units with complexity data
		unitComplexity = unit.find("./metric[@name='cyclomatic_complexity']")
		if unitComplexity != None:			

			# keep a tab of unit names we are adding under this file
			listTempUnitsInThisFile.append(unitName)
			unitSrNum = listTempUnitsInThisFile.count(unitName) # how many have we got now?
						
			# add to list
			logging.debug( '%s,%s,%s,%s,%s', fileName, unitName, unitSrNum, unitKind, unitComplexity.text )
			listData.append({
				"filename": fileName,
				"unit": unitName,
				"unit_serial_num": unitSrNum,
				"kind": unitKind,
				"cyclomatic_complexity": unitComplexity.text
				})


logging.info( "Done processing XML. Found complexity data for %s units", len(listData))
#print( listData )
writeCSV( listData )
