## MetaData 
Question Type : Multiple Choice
Max Answers : 4

## Question 
Microsoft Azure provides a robust alerting and monitoring solution called Azure Monitor. You can use Azure Monitor to configure notifications and alerts for your key systems and applications. These alerts will ensure that the correct team knows when a problem arises.<br>Which of the items below go into the composition of an alert rule? 

## Options 
Option 1 : Resource
Option 2 : Threshold
Option 3 : Condition
Option 4 : Actions
Option 5 : Alert Severity
Option 6 : Alert Priority 
Option 7 : Alert Details


## Answers 
Option 1 : 3
Option 3 : 3
Option 4 : 3
Option 7 : 3

## Reference Links 
https://learn.microsoft.com/en-us/training/modules/incident-response-with-alerting-on-azure/2-explore-azure-monitor-alert-types 

## Explanation 
You can use alert rules to create custom alerts and notifications. No matter which target resource or data source you use, the composition of an alert rule remains the same.<br>1.RESOURCE: The target resource for the alert rule. You can assign multiple target resources to a single alert rule. The type of resource defines the available signal types.<br>2. CONDITION: The signal type used to assess the rule. The signal type can be a metric, an activity log, or logs. There are others, but this module doesn't cover them.<br>The alert logic applied is to the data that are supplied via the signal type. The structure of the alert logic changes depending on the signal type.<br>3. ACTIONS: The action, like sending an email, sending an SMS message, or using a webhook.<br>An action group, which typically contains a unique set of recipients for the action.<br>4. ALERT DETAILS: An alert name and an alert description specify the alert's purpose.<br>The severity of the alert if the criteria or logic test evaluates true. The five severity levels are:<br>0: Critical <br>1: Error <br>2: Warning<br>3: Informational<br>4: Verbose