## MetaData 
Question Type : Single Choice

## Question
Case Study:<br>Your company uses an Azure storage account for storing large numbers of video and audio files. Containers are used to store each type of file and access is limited to those media files. Additionally, the files can only be accessed through shared access signatures.<br> Following are the requirements, which the company wants to apply.<br>• The ability to revoke access to the files and to change the period for which users can access the files.<br>• The company is planning a delegation model for Azure storage. Applications in the production environment must have unrestricted access to Azure Storage resources.<br>• You're researching how to use network configuration rules, Shared Access Signatures (SAS), and stored access policies to implement secure access to Azure Storage.<br><br>Question<br>You want to implement secure storage for the company’s media files in the easiest way. Which solution you will choose? Select one answer

## Options
Option 1 : Create a Stored Access Policy 
Option 2 : Create a Shared Access Signature
Option 3 : Configure Key vault
Option 4 : Configure Storage Encryption.

## Answers
Option 1 : 13

## Reference Links
https://learn.microsoft.com/en-us/training/modules/configure-storage-security/7-apply-best-practices

## Explanation
If a SAS is compromised, you can mitigate attacks by limiting the SAS validity to a short time. This practice is important if you can't reference a stored access policy. Near-term expiration times also limit the amount of data that can be written to a blob by limiting the time available to upload to it.

## Products 
Storage Accounts

## Modules SubModules CTA 
Implement and manage storage:Configure Azure Storage security:learn.microsoft.com/en-us/training/modules/configure-storage-security/
