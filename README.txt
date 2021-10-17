In order to run the NFT sales tracker program you must have the following dependencies installed
	- requests
	- time
	- pandas
and depending on where you want to export to (csv, excel, google sheets)
	CSV/Excel
	- openpyxl
	Google Sheets
	- gspread/gspread_dataframe


After following the required dependencies

	- Clone the repo with -> git clone "https://github.com/BSSOfficial/TAMU-Data-Synthesis"
	- cd into the repository with -> cd TAMU-Data-Synthesis
	- run the file that exports to csv with -> python3 TDSynthesis.py
	- run the file that adds to a google sheet in real time with -> python3 dataTest.py
	These projects will run on indefinitely until a keyboard interrupt such as ctrl+c, 
	constantly adding to the csv and google sheets
	Our graphics are made with the real time data displayed in google sheets as per our demo video.