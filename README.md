# OrganizePhotos
Usefull script for grouping photos by day/month/year.

# Flow:
- Select folder with photos.
- Select the ordering strategy (year, year and month, year month and day).
- Select the button to start!

# config.ini
- configure default Grouping Level by adjusting grouping_level setting. Only values from 1-3 are valid. In case of missing or invalid grouping_level setting - value 1 is going to be assigned.

# Deploy:
```console
pyinstaller main.py
```
- program is going to be inside *dist* folder
