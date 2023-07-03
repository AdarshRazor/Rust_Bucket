## MetaData
Question Type : Multiple Choice
Max Answers : 5
 
## Question
As a lead server administrator in your organization, you are tasked with migrating your company’s Active Directory Domain Services (AD DS) to the newer Windows Server 2022. You are concerned about the migration process and want to ensure that the users retain access to resources in the source AD DS forest and the destination AD DS forest.<br> What are the five planning steps you should consider before you migrate to a new AD DS forest? Select the correct five answers from the below options.            

## Options
Option 1 : Select new names
Option 2 : Delete idle and obsolete user accounts
Option 3 : Plan OU structure 
Option 4 : Identify objects to migrate 
Option 5 : Creating a maintenance window 
Option 6 : Identify apps that will be migrated   
Option 7 : Plan Group Policies   

## Answers
Option 1 : 2
Option 3 : 2
Option 4 : 3
Option 6 : 3
Option 7 : 3

## Reference Links
https://learn.microsoft.com/en-us/training/modules/active-directory-domain-services-migration/4-migrate-to-active-directory-domain-services 

## Explanation
Careful planning is required before you migrate to a new AD DS forest. Planning includes:<br>1.Select new names. Most migration tools require the source and destination AD DS forests to have unique domain names, NetBIOS names, and User Principal Name (UPN) suffixes.<br>2.Plan organizational unit (OU) structure. You can replicate the OU structure in the source AD DS forest, but this is an opportunity to restructure to better meet organizational needs if you choose to.<br>3.Plan Group Policies. Evaluate which Group Policy settings should be applied in the new AD DS forest and how they'll be applied in the new OU structure.<br>4.Identify objects to migrate- Depending on the scope of the project, only a subset of users, groups, computers, and servers might be migrated. For these objects, you also need to determine the attributes that should be migrated and excluded.<br>5.Identify apps that will be migrated. Apps can have many interdependent components, so you must also identify their components. Only after accurate identification can you plan how each app will be migrated.  

## Products
Azure Migrate
                
## Modules SubModules CTA
Migrate servers and workloads:Migrate an AD DS infrastructure to Windows Server 2022 AD DS:learn.microsoft.com/en-us/training/modules/active-directory-domain-services-migration/
