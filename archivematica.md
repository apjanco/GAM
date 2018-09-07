**New Archivematica Workflow**

1. Boot the BADL (if not already running)

2. Open VirtualBox

3. Start archivematicaVM by double-clicking.  

4. In Firefox, go to <a href="http://archivogam.haverford.edu/es/control-de-misi%C3%B3n/" target="_blank">archivogam.haverford.edu/</a>.  You'll need to log in and click on mission control. Find if there are bags ready for import (marked 'no importado'). For this tutorial, we'll use `bag95` as an example.
 
5. Open the terminal. 

6. Type `$ bash restart.sh`.  This is a bash script that will (re)start Archivematica.  It's a long story not suited for a tutorial.  

7. Change to the Downloads directory `$ cd Downloads`

8. You'll need to find the filename for the bag.  To do this, type`$ s3cmd ls s3://ds-gam/Bags/`.  In the list, find `s3://ds-gam/Bags/Agos21_2018_bag95.zip`.  I typically highlight and copy the name of the file for the next step. 

9. To download the file, type `$ s3cmd get <bag filename>` or in this case `$ s3cmd get s3://ds-gam/Bags/Agos21_2018_bag95.zip`.  The bags are typically 5-6GB and take 10-15 minutes to download. 

--- 

10. Once the file is downloaded, go to localhost in Firefox. You should see Archivematica.  

11. In the upper-left-hand corner, you should see a dropdown for 'Transfer Type'.  The default is 'Standard', change it to 'Zipped Bag.'

12. Click on Browse. You should see a directory tree. Find the Downloads folder and select Agos21_2018_bag95.zip. Click 'Add'.

13. Now click the 'Start transfer' button.  This can take a minute or two.  If nothing happens, check the upper-right-hand corner.  It should say 'Connected' with a green dot.  If it says 'initalizing' 'can't connect to database' or a variety of other beloved messages, go back to the terminal type `$ cd` and then `$ bash restart.sh`.  This will restart and hopefully repair the problem.   

14. After some time, you'll see 'Job: Approve zipped bagit transfer' with a dropdown 'Actions.'  Click on '-Approve Transfer'. Note that extract zipped bag can take up to 15 minutes and can appear stalled

15. Once you see 'Create SIP from Transfer', the process switches over to the Ingest tab.  Just click on 'Ingest' in the navbar.

16. Once Store DIP is complete, you can transfer the files to gotita
go to /home/digitalscholarship and enter
`sudo python upload_dip.py`
You should see the bag, enter the number next to it
You'll then be prompted to enter the password for the compas user, which is `apoyomutuo`

The files will now upload to the GAM server. 

If all went well, delete the zip file from Downloads
## Transfer AIP and DIP to storage 


Log in to gotita at 192.241.128.56 
switch to root `sudo su -`
activate the virtual env `source /usr/local/lib/python-virtualenv/gam_app/bin/activate`
`cd  /srv/GAM`
now `python manage.py import_dip`
Select the bag you just uploaded and wait for the script to complete.
It is good practice to confirm in the control panel that the bag was upladed.  You can also inspect
the new files in admin by selecting imagen, filter by the bag, and click the link. 

Problem cases:

	get() returned more than one Imagen
		- There is already an image with that name.  This often happens when documents are scanned twice in Guatemala. 
		- Check if both documents are the same, this typically occurs due to a typo. 


