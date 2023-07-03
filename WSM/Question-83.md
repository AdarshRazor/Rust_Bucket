## MetaData
Question Type : Single Choice

## Question
Contoso wants to use Azure Container Instances to run containers that need to be deployed quickly and only run for a short time. The containers do not need to be connected to a virtual network or have access to any specific resources. Which of the following is a valid command that can be used to create a container group in this scenario? 

## Options
Option 1 : az container create --resource-group myResourceGroup --name mycontainergroup --image microsoft/aci-helloworld --restart-policy OnFailure --ports 80 
Option 2 : az container create --resource-group myResourceGroup --name mycontainergroup --image microsoft/aci-helloworld --restart-policy OnFailure --dns-name-label contoso --ports 80 
Option 3 : az container create --resource-group myResourceGroup --name mycontainergroup --image microsoft/aci-helloworld --restart-policy OnFailure --vnet myVirtualNetwork --ports 80 
Option 4 : az container create --resource-group myResourceGroup --name mycontainergroup --image microsoft/aci-helloworld --restart-policy OnFailure --cpu 2 --memory 4 --ports 80 

## Answers
Option 1 : 13

## Reference Links
https://learn.microsoft.com/en-us/training/modules/configure-azure-container-instances/3-review

## Explanation
In this scenario, the command to create the container group should specify the image to be used, the restart policy to be applied, and the ports that need to be exposed. The container group does not need to be connected to a virtual network or have a custom DNS name. Option A satisfies these requirements and creates a container group named "mycontainergroup" in the resource group named "myResourceGroup". The --ports 80 parameter exposes port 80 to the public Internet.

## Products 
Azure Active Directory

## Modules SubModules CTA 
Manage Azure identities and governance:Configure Azure Active Directory:learn.microsoft.com/en-us/training/modules/configure-azure-active-directory/
