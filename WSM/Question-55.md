## MetaData 
Question Type : Multiple Choice
Max Answers : 4

## Question 
Which of the following items are prerequisites in order to connect a Kubernetes cluster to Azure Arc?

## Options 
Option 1 : An existing Kubernetes cluster.
Option 2 : Outbound connectivity from the cluster to Azure and to the Microsoft container registry that hosts the container images required for installation.
Option 3 : Docker engine installed on the Kubernetes cluster.
Option 4 : A user account or service principal in the Azure Active Directory (Azure AD) tenant for the subscription that hosts Azure Arc-enabled Kubernetes.
Option 5 : The latest version of Azure CLI or Azure PowerShell installed on your management computer.

## Answers 
Option 1 : 3
Option 2 : 3
Option 4 : 3
Option 5 : 4

## Reference Links 
https://learn.microsoft.com/en-us/training/modules/intro-to-arc-enabled-kubernetes/3-architecture-components

## Explanation 
To connect a Kubernetes cluster to Azure Arc, you need:<br>•	An existing Kubernetes cluster.<br>•	Outbound connectivity from the cluster to Azure and to the Microsoft container registry that hosts the container images required for installation. For details regarding target URLs and ports, refer to your product documentation.<br>•	A user account or service principal in the Azure Active Directory (Azure AD) tenant for the subscription that hosts Azure Arc-enabled Kubernetes. This account must have at least the Kubernetes Cluster - Azure Arc Onboarding Azure role-based access control (Azure RBAC) built-in role.<br>•	The latest version of Azure CLI or Azure PowerShell installed on your management computer. 

## Modules SubModules CTA
