## MetaData
Question Type : Multiple Choice
Max Answers : 3

## Question
Contoso has implemented a self-service password reset system in Azure AD to reduce the number of password reset requests reaching the help desk. The IT team of the company must meet some prerequisites, and undertake the task of configuring a self-service password reset in Azure AD for Contoso must be done. <br>Which of the following options should you configure? Select all that apply.  

## Options
Option 1 : Authentication methods 
Option 2 : Security questions 
Option 3 : Verified contact methods 
Option 4 : Password policies 

## Answers
Option 1 : 4
Option 2 : 4
Option 3 : 5

## Reference Links
https://learn.microsoft.com/en-us/azure/active-directory/authentication/tutorial-enable-sspr

## Explanation
To configure self-service password reset in Azure AD, you must configure the following:<br>1. You must select the authentication methods that users will use to verify their identities when resetting their passwords. These methods include email or mobile phone, a security question, or the Microsoft Authenticator app.<br>2. During password reset, you can configure users to answer security questions as an additional authentication factor.<br>3. Verified contact methods: You must configure the contact methods that users can use to receive a verification code for a password reset. These methods can include email or mobile phone. While password policies are essential for maintaining the security of the user's password, they are not directly related to configuring self-service password reset.

## Products 
Azure Active Directory

## Modules SubModules CTA 
Manage Azure identities and governance:Configure Azure Active Directory:learn.microsoft.com/en-us/training/modules/configure-azure-active-directory/
