<div align = "center"><h1>CoppeliaSim Playground</h1></div>  

### Overview
CoppeliaSim playground is a desktop application that was created to re-use some of the older e-Yantra Robotics competition themes (eYRC) and deploy them in a self-learning based application by leveraging an **interactive GUI** and providing relevant **resources and hints** wherever required.

### App Features
- Currently featured EYRC Themes- **Fruit Plucking Robot**.
- App works in both online mode and offline mode.
- Task Output saved to Google Sheets.
- Clickstream Data saved to Google Sheets.

### Technical Stack
Python, ElectronJS, Lua, CoppeliaSim Simulator

## App Screenshots

<div align="center">

<img src="./Images/img_1.png" alt="im1" width=500>
<br><b>Figure 1: CoppeliaSim Playground Welcome Screen</b>
</div>

<div align="center">
<img src="./Images/img_2.png" alt="img2" width=380> <img src="./Images/img_3.png" alt="img3" width=380>
<br><b>Figure 2: Theme Selection</b>
</div>

<div align="center">

<img src="./Images/img_5.png" alt="img5" width=500>
<br><b>Figure 3: Level Selection</b>
</div>

<div align="center">
<img src="./Images/img_6.png" alt="img6" width=380> <img src="./Images/img_7.png" alt="img7" width=380>
<br><b>Figure 4: Levels in a theme</b>
</div>

### Setup

You will need python and coppeliasim software already installed for complete functionality of this application.
 
Execute 'pip install -r requirements.txt' to install all the required packages for python

The repository currently has 4 folders:-

1) **Complete app** - This folder consists all the code for frontend, backend, main script and for electron packaging.The backend folder consists all the script files for the frontend HTML pages. The backend scripts and main script are well commented for anyone to take the work forward. For building the app (in windows)-
    - First have a look at the Readme.md file given in the folder.
    - Open command prompt in the complete app folder.
    - Install the required modules given in Readme.md file.
    - Execute **’npx electron-builder build –win portable’** to build the
    exe file.

2. Executable app-
This folder consists two build folders where one contains and exe build with all the levels in the theme unlocked and completed and hints unlocked. This app is only usable in offline mode. The second folder consits the exe build with all levels locked, they get unlocked as you complete the theme. This one is usable in both online as well as offline mode.

3. Complete frontend-
This folder consists all the frontend HTML and CSS files and their resources.

4. Themes-
This folder consists the theme files for the theme implemented in the app i.e, Fruit Plucking Robot Theme and arena scene files for two other themes.

**Project Collaborators** - Abhinav Sarkar, Mohd Zaid Chachiya, Anushka P, Aniket Roy
This project was done as a part of the e-Yantra Summer Internship Program (eYSIP-2022)

