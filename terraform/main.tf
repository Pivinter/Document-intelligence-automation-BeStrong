# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}
resource "azurerm_storage_account" "terraform_state" {
  name                     = "tfstatebestrong324"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.account_tier_terraform_state
  account_replication_type = var.account_replication_type_terraform_state
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.terraform_state.id
  container_access_type = "private"
}

resource "random_id" "suffix" {
  byte_length = 4
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# File Share
resource "azurerm_storage_share" "fileshare" {
  name               = "pdf-files"
  storage_account_id = azurerm_storage_account.main.id
  quota              = 5120
}

# Blob Container
resource "azurerm_storage_container" "jsoncontainer" {
  name                  = "ocr-json-results"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}

# Document Intelligence / Form Recognizer
resource "azurerm_cognitive_account" "docai" {
  name                  = "docai-service"
  location              = var.location
  resource_group_name   = azurerm_resource_group.main.name
  kind                  = "FormRecognizer"
  sku_name              = "S0"
  custom_subdomain_name = "docaiocr-${random_id.suffix.hex}"
}


# App Service Plan (for Function App)
resource "azurerm_service_plan" "functionplan" {
  name                = "function-app-plan"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "Y1"
}


# Azure Function App (Linux, Python)
resource "azurerm_linux_function_app" "functionapp" {
  name                        = var.function_app_name
  location                    = var.location
  resource_group_name         = azurerm_resource_group.main.name
  service_plan_id             = azurerm_service_plan.functionplan.id
  storage_account_name        = azurerm_storage_account.main.name
  storage_account_access_key  = azurerm_storage_account.main.primary_access_key
  functions_extension_version = "~4"
  site_config {
    application_stack {
      python_version = "3.10"
    }
  }
  identity {
    type = "SystemAssigned"
  }
}
