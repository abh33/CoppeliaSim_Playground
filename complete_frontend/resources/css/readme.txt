**CSS Files**

Almost all screens utilise general.css and fredoka.css
All the guide mes use guide_me.css.
All the task screens connected by screen 5 like screen_5_1.html, screen_5_2_1.html, etc. use screen_5_x.css.

Fredoka is a google font that is used extensively in our app. The steps to install that are:
Choose your font at http://www.google.com/fonts
Add the desired one to your collection using "Add to collection" blue button
Click the "See all styles" button near "Remove from collection" button and make sure that you have selected other styles you may also need such as 'bold'...
Click the 'Use' tab button on bottom right of the page
Click the download button on top with a down arrow image
Click on "zip file" on the the popup message that appears
Click "Close" button on the popup
Slowly scroll the page until you see the 3 tabs "Standrd|@import|Javascript"
Click "@import" tab
Select and copy the url between 'url(' and ')'
Copy it on address bar in a new tab and go there
Do "File > Save page as..." and name it "desiredfontname.css" (replace accordingly)
Decompress the fonts .zip file you downloaded (.ttf should be extracted)
Go to "http://ttf2woff.com/" and convert any .ttf extracted from zip to .woff
Edit desiredfontname.css and replace any url within it [between 'url(' and ')'] with the corresponding converted .woff file you got on ttf2woff.com; path you write should be according to your server doc_root
Save the file and move it at its final place and write the corresponding <link/> CSS tag to import these in your HTML page
From now, refer to this font by its font-family name in your styles
