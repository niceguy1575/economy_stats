#!/usr/bin/python

import pip

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])       


# main definition
if __name__ == "__main__":
	packages = ['yfinance', 'pandas', 'requests', 're', 'numpy', 'matplotlib', 'PyMuPDF', 'notion', 'bs4', 'datetime', 'dateutil', 'CNNFearAndGreedIndex', 'cairo']

	for p in packages:
		#print(p)
		import_or_install(p)
