"""Script to process the XML output of Adacore gnatmetric command

Usage:
	python <scriptname.py>

TODO 
	- Error handling
	- Accept input and output via command line params
"""
import sys
import xml.etree.ElementTree as ET
import csv
import logging

def setLoggingConfig():
	"""Set logging level and format
	"""
	logging.basicConfig( format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO ) 


def writeCSV( listOfDictDataItems, outputFilename ):
	"""Write Data to CSV file

		Args:
			listOfDictDataItems (List): A list of dictionary items, each of which represents the field values
			outputFilename (str): file name for writing CSV data to
	"""

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


def main(inputFilename, outputFilename):
	"""Reads XML data from input file and write CSV formatted data to output file

	Args:
		inputFilename (str): Input file name (contents expected to be XML)
		outputFilename (str): Output file name (contents WILL be CSV)
	
	Raises:
		FileNotFoundException: When the input file is not found
	"""
	logging.info("Opening file: %s)", inputFileName)
	tree = ET.parse(inputFileName)
	logging.info('Parsed XML')
	root = tree.getroot()
	listData = [] # will hold data of interest extracted from the input XML file
	## XML tag names in the input file

	# For each <file> under root
	for file in root.iter('file'): 

		fileName = file.attrib.get('name')
		logging.debug( 'Processing file tag with name = %s', fileName)

		# set/reset vars we use for each change in file
		sr_num = 0 
		listTempUnitsInThisFile = []

		# for every <unit> under <file> - no matter how deep!
		for unit in file.findall(".//unit"):

			# extract unit details
			unitName = unit.attrib["name"]
			unitKind = unit.attrib["kind"]

			logging.debug( 'Found unit tag under it with name = %s', unitName)
			# Look for units with complexity data
			unitComplexity = unit.find("./metric[@name='cyclomatic_complexity']")
			logging.debug( 'Looking for complexity metric of this unit')
			if unitComplexity != None:			

				# keep a tab of unit names we are adding under this file
				listTempUnitsInThisFile.append(unitName)
				unitSrNum = listTempUnitsInThisFile.count(unitName) # how many have we got now?
							
				# add to list
				logging.debug( 'Result - %s,%s,%s,%s,%s', fileName, unitName, unitSrNum, unitKind, unitComplexity.text )
				listData.append({
					"filename": fileName,
					"unit": unitName,
					"unit_serial_num": unitSrNum,
					"kind": unitKind,
					"cyclomatic_complexity": unitComplexity.text
					})
			else:
				logging.debug('None found, moving on')

	logging.info( "Finished processing XML. Found complexity data for %s units", len(listData))
	#print( listData )
	writeCSV( listData, outputFilename )


if __name__ == '__main__':


	setLoggingConfig()

	## I/O File names 
	##
	# TEST set
	# inputFileName = '20221209 (Ada) - Test.xml' 
	# outputFilename = '20221209 (Ada) - Test.csv'
	#
	# FINAL set (TIP: Use forward slashes instead backslashes in paths)
	# inputFileName = 'D:/TMP/20230106/Data files/20230106 - metrix.xml' # final file
	# outputFilename = 'D:/TMP/20230106/Data files/20230106 - metrix.csv'

	# accept command line args
	try:
		inputFileName = sys.argv[1]
		outputFilename = sys.argv[2]
	except:
		logging.error( f"Usage: python '{__file__}' <input XML filename> <output CSV filename>" )
		sys.exit(1)

	try:
		main(inputFileName, outputFilename)
	except ET.ParseError as pe:
		logging.error("Cannot parse XML. Please check input file contains valid XML data")
	except BaseException as e:
		logging.error(e)

