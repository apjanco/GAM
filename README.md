# GAM


## Instructions for processing with Archivematica
- To see the current contents of cloud storage: `$ s3cmd ls s3://ds-gam/Bags/`
- To download a bag: `$ s3cmd get s3://ds-gam/Bags/<bag_name> /home/digitalscholarship/BAGS/` 
  Alternatively, you can use the Digital Ocean web application.  For large files (5+GB) you may get a 'read operation timed out' error with s3cmd.   
- Go to `localhost` in Firefox 
- With Transfer tab selected, change 'Transfer Type' to 'Zipped Bag'.
- Click Browse, click on digitalscholarship and then BAGS (or the directory containing the bag's zip file)
- Select the bag to process.  To process multiple bags, click on one, click add, then select the next. 
- Start Transfer
- Scroll down and you'll see Job: Approve zipped bag transfer, click Actions > Approve Transfer
- When at little red 1 appears on the Injest tab, click on Injest
- Find Job: Approve normalization > Approve
- Job Upload DIP > Do not upload DIP 
- When you see a little green checkmark next to the bag name, the processing is complete.
- Find the DIP in the DIPstore.  Open the objects folder and manually inspect each image.  All images should be oriented vertically.  If some are horizontal, double-click on the image.  When you hover over the image, two arrow will appear at the bottom.  Use the buttons to change the orientation and ctrl-s to save. 
#
TODO instructions for upload_dip script

# The DIP is now on the server. 
- Type `sudo su -`
- Start the applications virtual enviornment by typing `cd /usr/local/lib/python-virtualenv/gam_env/`
- Now type `source bin/activate`
- or `source /usr/local/lib/python-virtualenv/gam_env/bin/activate`
- Now move to the project directory: `/srv/GAM`
-To activate the import script, type: `python manage.py import_dip`
- Enter the number of the DIP you would like to import 
- Cross your fingers 
 
