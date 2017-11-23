#!/usr/bin/env python
# Solution task from Serhii Konovalenko for position Junior DevOps

import datetime as dt
import sys
from termcolor import colored
import boto3


ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


for instance in ec2.instances.all():
    # ---Checking if tags exist---
    if instance.tags != None:

        for tag in instance.tags:

	    #---Save instance name---
	    
	    if tag[u'Key'] == 'Name':
	        inst_name = tag[u'Value']

            #---Searching Buckup tag with value=true---
            if (tag[u'Key'] == 'Backup') and (tag[u'Value'] == 'true'):

		#---Creating Buckup Image of Instance---
		time = str(dt.datetime.today())
	        #---Creating name of image---
		name_backup = 'Name ' +  time.replace(':', '.')

		response = client.create_image(
			BlockDeviceMappings=[
				{
           			 'DeviceName': '/dev/xvda',
            			 'Ebs': {
               				 'Encrypted': False,
               				 'DeleteOnTermination': True
                  			 },
            
       				 }, ],
   			 Description='My buckup image',
			 InstanceId=instance.id,
   			 Name=name_backup,
    			 NoReboot=True ) 


#---Reading information abour own Images---
response = client.describe_images(Owners=['071759926740',])#---i used my own id---

#---variable for saving old ImageId---
del_image=[]

for image in response[u'Images']:
    #---Calculating time living (old) of image---
    deltatime=dt.datetime.strptime(str(dt.datetime.today())[:10], "%Y-%m-%d") - dt.datetime.strptime(image[u'CreationDate'][:10], "%Y-%m-%d")

    #---forming statics as a table [ImageId, Name, CreationDate, State, Old]---
    text =  image[u'ImageId'] + '||'+ image[u'Name']+ '||'+ image[u'CreationDate'][:10]+ '||'+ image[u'State']+ '||'+str(deltatime)

    #---Checking our condition > 7 days, output color statistics of ami---

    if int(str(deltatime)[0]) > 7:
	del_image.append(image[u'ImageId'])	
        text = colored(text, 'yellow')
        print text        
    else:
        text = colored(text, 'green')
        print text

#---deleting old ami---
for im_id in del_image:
    client.deregister_image(ImageId=im_id)




