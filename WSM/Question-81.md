## MetaData
Question Type : Dropdown
 
## Question
You have an Azure Virtual Network having a Virtual Machine named WebApp1. WebApp1 has the following configurations:<br>• Subnet : 10.0.0.0/24<br>• Availability Set : WebA1<br>• Private IP Address: 10.0.0.1<br>• Public IP Address: 40.90.219.6<br>• Network Security Group(NSG): Not Configured<br><br>You deployed a Standard Azure Load Balancer named ALB1. You need to configure ALB1 to connect to Web App1. What are the changes you should apply in WebApp1?<br><br>For each statement select the appropriate answer from the dropdown.<br><br>Before You create a Backend pool on ALB1, you must [[DropDown 1]]<br><br>Before you connect WebApp1 from ALB1, you must [[DropDown 2]]

## Options
DropDown 1 : Create and assign an NSG to WebApp1
DropDown 1 : Remove the Public IP Address from WebApp1
DropDown 1 : Change the Private IP Address of WebApp1 to static
DropDown 2 : Create and configure an NSG
DropDown 2 : Remove the Public IP Address from WebApp1
DropDown 2 : Change the Private IP Address of WebApp1 to static
 
## Answers
DropDown 1 : Remove the Public IP Address from WebApp1 : 6
DropDown 2 : Create and configure an NSG : 7

## Reference Links
https://learn.microsoft.com/en-us/training/modules/configure-azure-load-balancer/3-implement-public


## Explanation
A public load balancer maps the public IP address and port number of incoming traffic to the private IP address and port number of the VM. Mapping is also provided for the response traffic from the VM. By applying load-balancing rules, you can distribute specific types of traffic across multiple VMs or services. For example, you can spread the load of incoming web request traffic across multiple web servers.

## Products 
Load Balancer

## Modules SubModules CTA 
Configure and manage virtual networking:Configure Azure Load Balancer:learn.microsoft.com/en-us/training/modules/configure-azure-load-balancer/
