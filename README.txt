fIn order to run the NFT sales tracker program you must have the following dependencies installed
	- import/install requests
	- import/install time
	- import/install pandas
and depending on where you want to export to (csv, excel, google sheets)
	CSV/Excel
	- import/install openpyxl
	Google Sheets
	- import/install gspread/gspread_dataframe


After following the required dependencies

	- Clone the repo with -> git clone "https://github.com/BSSOfficial/TAMU-Data-Synthesis"
	- cd into the repository with -> cd TAMU-Data-Synthesis
	- run the file that exports to csv with -> python3 NFTSalesTracker-CSV.py
	- run the file that adds to a google sheet in real time with -> python3 NFTSalesTracker-GoogleSheets.py
	These projects will run on indefinitely until a keyboard interrupt such as ctrl+c, 
	constantly adding to the csv and google sheets
	Our graphics are made with the real time data displayed in google sheets as per our demo video.

	If you are interested in seeing the google sheets data run in real time, message Dalton Avery, Tommy Truong, Thanh Nguyen, or Tien Nguyen so we can share the link with you all and run the data, as the google sheets api requires authentication.