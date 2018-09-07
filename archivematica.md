**New Archivematica Workflow**

1. Boot the BADL (if not already running)

2. Open VirtualBox

3. Start archivematicaVM, by double-clicking.  

4. In Firefox, go to archivogam.haverford.edu.  You'll need to log in and click on mission control. Find if there are bags ready for import (marked 'no importado').
 
5. Open the terminal. 

6. Type `$ bash restart.sh`.  This is a bash script that will start Archivematica. 

7. Change to the Downloads directory `$ cd Downloads`

finds the filename for the bag using `s3cmd ls s3://ds-gam/Bags/`
then `s3cmd get <bag filename>`
Once downloaded, go to local host 
In 'Transfer Type' select 'Zipped Bag'
Click on Browse,  find the Downloads folder 
Select the bag and click add
Then start transfer 
Wait 3-4 minutes, this can take a while
When prompted, approve transfer 
Note that extract zipped bag can take up to 15 minutes and can appear stalled

Once it gets to Create SIP from Transfer to process switches to the Ingest tab
Once Store DIP is complete, you can transfer the files to gotita
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


