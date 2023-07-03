## MetaData
Question Type : Multiple Single Choice
 
## Question
Assess the veracity of the following statements about Azure AD’s self-service password reset capability. 

## Labels
Label 1 : The self-service password reset feature is available in all editions of Azure AD  
Label 2 : The security questions authentication method isn't available to accounts that are associated with an administrator role. 
Label 3 : A strong, two-method authentication policy is always applied to accounts with an administrator role, regardless of your configuration for other users. 
Label 4 : There are two settings for the Self-service password reset enabled property: Enabled and Disabled 
 
## Options
Option 1 : True
Option 2 : False
 
## Answers
Label 1 : Option 2 : 3
Label 2 : Option 1 : 3
Label 3 : Option 1 : 3
Label 4 : Option 2 : 3
 
## Reference Links
https://learn.microsoft.com/en-us/training/modules/allow-users-reset-their-password/3-implement-azure-ad-self-service-password-reset
https://learn.microsoft.com/en-us/training/modules/allow-users-reset-their-password/2-self-service-password-reset   
 
## Explanation
The editions of Azure AD are free, Premium P1, and Premium P2. The password reset functionality you can use depends on your edition.<br>A strong, two-method authentication policy is always applied to accounts with an administrator role, regardless of your configuration for other users.<br>The security questions method isn't available to accounts that are associated with an administrator role.<br>There are three settings for the Self-service password reset enabled property:<br>1. Disabled: No users in the Azure AD organization can use SSPR. This value is the default.<br>2. Enabled: All users in the Azure AD organization can use SSPR. <br>3. Selected: Only the members of the specified security group can use SSPR. You can use this option to enable SSPR for a targeted group of users, who can test it and verify that it works as expected. When you're ready to roll it out broadly, set the property to Enabled so that all users have access to SSPR. 