## MetaData
Question Type : Match Options

## Question
Most Azure regions are paired with another region within the same geography to make a regional pair (or paired regions). Regional pairs help to support always-on availability of Azure resources used by your infrastructure.<br>Identify the characteristics of paired regions based on their description. 

## Labels
Label 1 : Azure prefers at least 300 miles of separation between datacenters in a regional pair. This principle isn't practical or possible in all geographies. Physical datacenter separation reduces the likelihood of natural disasters, civil unrest, power outages, or physical network outages affecting both regions at once. 
Label 2 : Some services like Geo-Redundant Storage provide automatic replication to the paired region. 
Label 3 : During a broad outage, recovery of one region is prioritized out of every pair. Applications that are deployed across paired regions are guaranteed to have one of the regions recovered with priority. 
Label 4 : Planned Azure system updates are rolled out to paired regions sequentially (not at the same time). Rolling updates minimizes downtime, reduces bugs, and logical failures in the rare event of a bad update. 
Label 5 : Regions reside within the same geography as their enabled set (except for the Brazil South and Singapore regions). 

## Options
Option 1 : Data residency 
Option 2 : Physical isolation 
Option 3 : Region recovery order 
Option 4 : Platform-provided replication 
Option 5 : Sequential updates 

## Answers
Label 1 : Option 2 : 2
Label 2 : Option 4 : 2
Label 3 : Option 3 : 2
Label 4 : Option 5 : 3
Label 5 : Option 1 : 3

## Reference Links
 https://learn.microsoft.com/en-us/training/modules/configure-subscriptions/2-identify-regions  

## Explanation
<img src="https://github.com/CloudLabs-MOC-PT/Practice-Test-Images/blob/main/CLX/Images/E09.PNG?raw=true"/> 
