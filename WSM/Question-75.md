## MetaData
Question Type : Single Choice

## Question
Case Study 2:
Contoso, Ltd. is a global manufacturing company with offices all over the world. Contoso products are produced using blueprint files created and maintained by the company and they work with their partner organizations to bring their product to the market. You are working as a cloud administrator there.<br><br> Current Environment:<br>To facilitate business operations, Contoso uses several types of servers including the following:<br>File servers<br>Domain controllers<br>Microsoft SQL Server servers<br>There is an Active Directory forest called contoso.com on your network. Servers and client computers are joined to Active Directory. You have an application called App1 that is visible to the public. App1 is a public-facing application you have. The following three tiers are there in App1: <br>A SQL database <br>A web front end <br>A processing middle tier <br>Each tier consists of five virtual machines. Users can only access the web front end via HTTPS. <br><br>Requirements: <br>Planned Changes: <br>Contoso plans to implement the following infrastructure changes:  <br>Migrate all App1 tiers to Azure. <br>Move existing production plan files to Azure Blob storage.  <br>Create a hybrid catalog to support the upcoming Microsoft Office 365 migration project. <br><br>Technical requirements: <br>Contoso must meet the following technical requirements:  <br>Migrate all App1 VMs to Azure.  <br>Minimize the number of open ports between App1 tiers.  <br>Make sure all App1 virtual machines are protected with backups.  <br>Copy blueprint files over the Internet to Azure.  <br>Ensure that the plan files are saved to the storage level of the repository.  <br>Ensure partner access to plan files is secure and temporary.  <br>Avoid storing user passwords or password hashes in Azure. <br>Use unmanaged standard storage for virtual machine hard disks.  <br>Ensure that when users connect devices to Azure Active Directory (Azure AD), users use a mobile device for authentication.  <br>Reduce administrative efforts whenever possible. <br><br>User Requirements: <br>Contoso has identified the following requirements for users:  <br>Allows only users who are part of the group named Pilot to join the device to Azure AD.  <br>Set a new user named Admin1 as a service administrator for your Azure subscription.  <br>Admin1 should receive email notifications of service outages. <br>Verify that a new user named user3 can create network objects for your Azure subscription.<br><br>Question:<br>You must move the blueprint files to Azure as part of the task. Which of the following option you will choose?

## Options
Option 1 : Generate an access key. Map a drive, and then copy the files by using File Explorer.
Option 2 : Use Azure Storage Explorer to copy the files.
Option 3 : Use the Azure Import/Export service.
Option 4 : Generate a shared access signature (SAS). Map a drive, and then copy the files by using File Explorer.

## Answers
Option 2 : 13

## Reference Links
https://learn.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer?tabs=windows

## Explanation
Azure Storage Explorer is a free tool from Microsoft that allows you to work with Azure Storage data on Windows, macOS, and Linux. You can use it to upload and download data from Azure blob storage.<br>Scenario:<br>Planned Changes include: moving the existing product blueprint files to Azure Blob storage. Technical Requirements include: Copy the blueprint files to Azure over the Internet. 

## Products 
Azure Active Directory

## Modules SubModules CTA 
Manage Azure identities and governance:Configure Azure Policy:learn.microsoft.com/en-us/training/modules/configure-azure-policy/