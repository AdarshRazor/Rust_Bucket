## MetaData
Question Type : Multiple Choice
Max Answers : 2

## Question
This diagram highlights the contributor role of RBAC policy in your organization.<br><br><img src="https://github.com/CloudLabs-MOC-PT/Practice-Test-Images/blob/main/CLX/Images/Q70.png?raw=true"/><br><br> From the above diagram provided identify which of the following statements is true about it.<br> Select two right options.

## Options
Option 1 : Contributor role can authorize to increase the level or scope of access privileges
Option 2 : Contributor role can be assigned to all scopes that affect data.
Option 3 : Contributor role cannot authorize to delete or remove any resources
Option 4 : Contributor can authorize to write or change for all resources.

## Answers
Option 2 : 6
Option 3 : 7

## Reference Links
https://learn.microsoft.com/en-us/training/modules/configure-role-based-access-control/3-create-role-definition

## Explanation
The Actions permissions show the Contributor role has all action privileges. The asterisk "*" wildcard means "all".<br>• The NotActions permissions narrow the privileges provided by the Actions set, and deny three actions:<br>1. Authorization/*/Delete: Not authorized to delete or remove for "all".<br>2. Authorization/*/Write: Not authorized to write or change for "all".<br>3. Authorization/elevateAccess/Action: Not authorized to increase the level or scope of access privileges.<br><br>•         The Contributor role also has two DataActions permissions to specify how data can be affected:<br>1. "NotDataActions": []: No specific actions are listed. Therefore, all actions can affect the data.<br>2. "AssignableScopes": ["/"]: The role can be assigned for all scopes that affect data. The backslash {\} wildcard means "all". 

## Products 
Azure Active Directory

## Modules SubModules CTA 
Manage Azure identities and governance:Configure role-based access control:learn.microsoft.com/en-us/training/modules/configure-role-based-access-control/
