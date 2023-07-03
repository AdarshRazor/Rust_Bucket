## MetaData
Question Type : Multiple Choice
Max Answers : 2

## Question
You are working at a pharmaceutical company as an Azure Administrator. The following diagram shows an example of how scopes can be applied to a role to grant varying levels of access for different users.<br><br><img src="https://github.com/CloudLabs-MOC-PT/Practice-Test-Images/blob/main/CLX/Images/Q67.png?raw=true"/><br><br>Based on the above diagram identify which of the following statements is true.<br> Select two right options.

## Options
Option 1 : Six built-in roles are implemented, and two custom roles are defined: Reader Support Tickets and Virtual Machine Operator.
Option 2 : Users in the Marketing group are granted access to create or manage any Azure resource in the Pharma-sales resource group.
Option 3 : The contributor is not having permission to access any of the resources
Option 4 : The built-in Contributor role has three sets of permissions: Actions, Contributions and NotActions.

## Answers
Option 1 : 6
Option 2 : 7

## Reference Links
https://learn.microsoft.com/en-us/training/modules/configure-role-based-access-control/4-create-role-assignment

## Explanation
This scenario has the following access management configuration:<br>1. Three security principals are supported: user, group, and service principal.2. Six built-in roles are implemented, and two custom roles are defined: Reader Support Tickets and Virtual Machine Operator.<br>3. The built-in Contributor role has two sets of permissions: Actions and NotActions.<br><br>4. The Contributor role is assigned at different scopes to the Marketing group and Pharma-sales resource group:<br>a. Users in the Marketing group are granted access to create or manage any Azure resource in the Pharma-sales resource group.<br>b. Marketing users aren't granted access to resources outside the Pharma-sales resource group unless they have another role assignment that grants them access to the resource group.  

## Products 
Azure Active Directory

## Modules SubModules CTA 
Manage Azure identities and governance:Configure role-based access control:learn.microsoft.com/en-us/training/modules/configure-role-based-access-control/
