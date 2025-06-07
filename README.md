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