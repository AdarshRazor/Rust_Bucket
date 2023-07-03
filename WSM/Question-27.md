## MetaData
Question Type : Multiple Single Choice
 
## Question
Assess the veracity of the following statements about Azure Backup. 

## Labels
Label 1 : Azure Backup provides built-in monitoring and alerting capabilities in a Recovery Services vault.  
Label 2 : Azure Backup offers the ability to back up virtual machines encrypted with Azure Disk Encryption. 
Label 3 : Backup data can only be encrypted using Microsoft-managed keys.  
Label 4 : Azure Backup always replicates data using Geo-redundant storage (GRS) 
Label 5 : With soft delete, the backup data is retained for 30 more days even after the deletion of the backup item. 
 
## Options
Option 1 : True
Option 2 : False
 
## Answers
Label 1 : Option 1 : 2
Label 2 : Option 1 : 2
Label 3 : Option 2 : 2
Label 4 : Option 2 : 3
Label 5 : Option 2 : 3
 
## Reference Links
https://learn.microsoft.com/en-us/training/modules/protect-virtual-machines-with-azure-backup/2-azure-backup-features-scenarios 
 
## Explanation
Azure Backup provides built-in monitoring and alerting capabilities in a Recovery Services vault. These capabilities are available without any additional management infrastructure.<br><br>Azure Backup offers the ability to back up virtual machines encrypted with Azure Disk Encryption.<br><br>Backup data is automatically encrypted using Microsoft-managed keys. Alternatively, you can also encrypt your backed-up data using customer-managed keys stored in the Azure Key Vault.<br><br>With soft delete, the backup data is retained for 14 more days even after the deletion of the backup item. This protects against accidental deletion or malicious deletion scenarios, allowing the recovery of those backups with no data loss. 