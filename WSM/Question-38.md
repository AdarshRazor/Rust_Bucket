## MetaData 
Question Type : Multiple Single Choice

## Question 
Assess the veracity of the following statements about Azure Availability Zones. 

## Labels
Label 1 : Availability zones are independent physical datacenter locations within a region that include their own power, cooling, and networking.
Label 2 : Supported regions contain a minimum of three availability zones.
Label 3 : Availability zones are to be used jointly with availability sets. When using availability zones, you should also define an availability set for your systems.
Label 4 : Availability zones are available across all regions

## Options
Option 1 : True
Option 2 : False

## Answers 
Label 1 : Option 1 : 3
Label 2 : Option 1 : 3
Label 3 : Option 2 : 3
Label 4 : Option 2 : 3

## Reference Links 
https://learn.microsoft.com/en-us/training/modules/azure-well-architected-reliability/2-high-availability

## Explanation 
Availability zones are independent physical datacenter locations within a region that include their own power, cooling, and networking. By taking availability zones into account when deploying resources, you can protect workloads from datacenter outages while retaining a presence in a particular region.<br><br>Supported regions contain a minimum of three availability zones. When creating zonal service resources in those regions, you'll have the ability to select the zone in which the resource should be created. This will allow you to design your application to withstand a zonal outage and continue to operate in an Azure region before having to evacuate your application to another Azure region.<br><br>Availability zones are mutually exclusive with availability sets. When using availability zones, you no longer need to define an availability set for your systems. You'll have diversity at the data-center level, and updates will never be performed to multiple availability zones at the same time.<br><br>Availability zones are a newer high-availability configuration service for Azure regions and are currently available for certain regions. It's important to check the availability of this service in the region in which you're planning to deploy your application if you want to consider this functionality. 

## Modules SubModules CTA
