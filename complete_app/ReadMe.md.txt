**CoppeliaSim Playground**

App Features-
• Currently featured EYRC Themes- Fruit Plucking Robot.
• App works in both online mode and offline mode.
• Task Output saved to Google Sheets.
• Clickstream Data saved to Google Sheets.
• Visual Streaming (CoppeliaSim Add-on).

functionality:         
*Open Coppelisim Scene  ✓
*Evaluate               ✓
*Restart                ✓
*Open Python            x
*Read more              ✓
*Guide me               ✓
*Level Select           ✓
*Progress Bar           ✓
*star Grading system    ✓

*Execute these Command to install all required modules*
npm install electron --save-dev   
npm install --save @electron/remote  
npm install -save fs  
pip install -r requirements.txt

For building the app (in windows)-
• First have a look at the Readme.md file given in the folder.
• Open command prompt in the complete app folder.
• Install the required modules given in Readme.md file.
• Execute ’npx electron-builder build –win portable’ to build the exe file.

*you will need python and coppeliasim software already installed for complete functionality of this application