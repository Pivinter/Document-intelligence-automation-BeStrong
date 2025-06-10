# Document-intelligence-automation-BeStrong
Infrastructure and CI/CD for Azure Document Intelligence OCR using Terraform, Azure Functions, and notifications via Discord &amp; Telegram.

## Step 1: Initial Run (without backend)

```bash
terraform init
terraform apply \
  -target=azurerm_resource_group.main \
  -target=azurerm_storage_account.tfstate \
  -target=azurerm_storage_container.tfstate
```

## Step 2: Backend Configuration

```bash
terraform init   # with backend
```

## Report of our work

all resources created
![Моє фото](images/hz.png)

 **key file that contains all the keys**
![Моє фото](images/key.png)

 **pdf file**
![Моє фото](images/pdd.png)


 **funtions messages**
![Моє фото](images/work.png)

 **json file in our container**
![Моє фото](images/resul.png)

**message in telegram**
![Моє фото](images/tg.png)

**message in diskord**
![Моє фото](images/ds.png)

**and finally our result**
![Моє фото](images/result.png)









