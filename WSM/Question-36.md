## MetaData 
Question Type : Multiple Choice
Max Answers : 2

## Question 
Availability sets are a way for you to inform Azure that VMs that belong to the same application workload should be distributed to prevent simultaneous impact from hardware failure and scheduled maintenance.<br><img src="https://github.com/CloudLabs-MOC-PT/Practice-Test-Images/blob/main/CLX/Images/Q36.png?raw=true"><br>What are the 2 concepts (also shown in the figure above) that enable Availability sets to achieve their stated goals?

## Options 
Option 1 : Fault domains
Option 2 : Unified domains
Option 3 : Failover domains
Option 4 : Update domains
Option 5 : Fragmentation domains
Option 6 : Uninterruptable domains

## Answers 
Option 1 : 6
Option 4 : 6

## Reference Links 
https://learn.microsoft.com/en-us/training/modules/protect-infrastructure-with-site-recovery/3-site-recovery-setup

## Explanation 
Update domains ensure that a subset of your application's servers always remain running when the virtual machine hosts in an Azure datacenter require downtime for maintenance. Most updates can be performed with no impact to the VMs running on them, but there are times when this isn't possible. To ensure that updates don't happen to a whole datacenter at once, the Azure datacenter is logically sectioned into update domains (UD). When a maintenance event occurs, such as a performance update and critical security patch that needs to be applied to the host, the update is sequenced through update domains. The use of sequencing updates using update domains ensures that the whole datacenter isn't unavailable during platform updates and patching.<br>While update domains represent a logical section of the datacenter, fault domains (FD) represent physical sections of the datacenter and ensure rack diversity of servers in an availability set. Fault domains align to the physical separation of shared hardware in the datacenter. This includes power, cooling, and network hardware that supports the physical servers located in server racks. In the event the hardware that supports a server rack has become unavailable, only that rack of servers would be affected by the outage. By placing your VMs in an availability set, your VMs will be automatically spread across multiple FDs so that in the event of a hardware failure, only some of your VMs will be impacted.

## Modules SubModules CTA
