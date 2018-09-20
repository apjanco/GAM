**New Archivematica Workflow**

1. Boot the BADL (if not already running)

2. Open VirtualBox

3. Start archivematicaVM by double-clicking.  

4. In Firefox, go to <a href="http://archivogam.haverford.edu/es/control-de-misi%C3%B3n/" target="_blank">archivogam.haverford.edu/</a>.  You'll need to log in and click on mission control. Find if there are bags ready for import (marked 'no importado'). For this tutorial, we'll use `bag95` as an example.
 
5. Open the terminal. 

6. Type `$ bash restart.sh`.  This is a bash script that will (re)start Archivematica.  It's a long story not suited for a tutorial.  

7. Change to the Downloads directory `$ cd Downloads`

8. You'll need to find the filename for the bag.  To do this, type`$ s3cmd ls s3://bolsas/`.  In the list, find `s3://ds-gam/Bags/Agos21_2018_bag95.zip`.  I typically highlight and copy the name of the file for the next step. 

9. To download the file, type `$ s3cmd get <bag filename>` or in this case `$ s3cmd get s3://bolsas/Agos21_2018_bag95.zip`.  The bags are typically 5-6GB and take 10-15 minutes to download. 

--- 

10. Once the file is downloaded, go to localhost in Firefox. You should see Archivematica.  

11. In the upper-left-hand corner, you should see a dropdown for 'Transfer Type'.  The default is 'Standard', change it to 'Zipped Bag.'

12. Click on Browse. You should see a directory tree. Find the Downloads folder and select Agos21_2018_bag95.zip. Click 'Add'.

13. Now click the 'Start transfer' button.  This can take a minute or two.  If nothing happens, check the upper-right-hand corner.  It should say 'Connected' with a green dot.  If it says 'initalizing' 'can't connect to database' or a variety of other beloved messages, go back to the terminal type `$ cd` and then `$ bash restart.sh`.  This will restart and hopefully repair the problem.   

14. After some time, you'll see 'Job: Approve zipped bagit transfer' with a dropdown 'Actions.'  Click on '-Approve Transfer'. Note that extract zipped bag can take up to 15 minutes and can appear stalled

15. Once you see 'Create SIP from Transfer', the process switches over to the Ingest tab.  Just click on 'Ingest' in the navbar.

16. Once Store DIP is complete, you can transfer the files to the GAM server.

--- 

17. Type `$ cd` in the terminal.  Then type `$ sudo python upload_dip.py`

18. You will see a list of possible bags to upload.  Type the number to the left of the bag name.  In this case, I see `(5, 'bag95'...)`, so enter 5.

19. Enter the password for the compas user on the server.  You should see the files being uploaded. 

20. Now is a good time to delete the original bag.  `$ cd Downloads` then `$ rm Agos21_2018_bag95.zip`.

---

21. Connect to the GAM server with your username: `$ ssh username@192.241.128.56`

22. Switch to root `$ sudo su -`, activate the GAM virtual enviornment `$ source /usr/local/lib/python-virtualenv/gam_env/bin/activate`.

23. Now `$ cd /srv/GAM` and type `$ python manage.py import_dip`.

24. Select the number next to the bag you'd like to import.  Keep in mind that the server only has 20GB of storage.  It is important to clear out bags once they're imported of you'll get an 'out of storage' message. 

25.  Once the script completes, the files are now ready.  It is good practice to log in to admin and check that images from the bag you just imported are visible on the site. 

--- 

26. The VM on the BADL only has 300GB of space.  Once you're finished processing 2-3 bags, you'll need to move the completed AIPs and DIPs to the 4TB drive.

... to do this ...

---
Problem cases:

	get() returned more than one Imagen
		- There is already an image with that name.  This often happens when documents are scanned twice in Guatemala. 
		- Check if both documents are the same, this typically occurs due to a typo. 


