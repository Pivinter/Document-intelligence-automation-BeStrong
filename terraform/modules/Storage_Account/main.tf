resource "azurerm_storage_account" "main" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags               = {
    Environment = var.environment
  }
}

resource "azurerm_storage_share" "fileshare" {
  name               = "pdf-files"
  storage_account_id = azurerm_storage_account.main.id
  quota              = 5120
}

resource "azurerm_storage_container" "jsoncontainer" {
  name                  = "ocr-json-results"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}