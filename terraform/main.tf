# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "terraform_state" {
  name                     = "tfstatebestrong3246"
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

module "Storage_Account" {
  source              = "./modules/Storage_Account"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

module "App_Service_Plan" {
  source                     = "./modules/App_Service_Plan"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  storage_account_name       = module.Storage_Account.storage_account_name
  storage_account_access_key = module.Storage_Account.storage_account_access_key
}

module "Document_Intelligence" {
  source              = ".
