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
import csv, sys
import logging

# Reference Values

## Flags
logging.basicConfig( format='%(asctime)s %(message)s', level=logging.INFO ) 

## File names
inputFileName = 'Input_Sample.xml'
outputFilename = 'Output.xml'

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

	# for every <unit> under <file> - no matter how deep!
	for unit in file.findall(".//unit"):
		# extract unit details
		unitName = unit.attrib["name"]
		unitKind = unit.attrib["kind"]
		unitComplexity = unit.find("./metric[@name='cyclomatic_complexity']")
		if unitComplexity != None:
			#logging.debug( '%s,%s,%s,%s', fileName, unitName, unitKind, unitComplexity.text )
			# add to list
			listData.append({
				"filename": fileName,
				"unit": unitName,
				"kind": unitKind,
				"cyclomatic_complexity": unitComplexity.text
				})


logging.info( "Done processing XML. Found complexity data for %s units", len(listData))
#print( listData )
writeCSV( listData )
