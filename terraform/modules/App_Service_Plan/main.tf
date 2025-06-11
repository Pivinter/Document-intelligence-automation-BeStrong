resource "azurerm_service_plan" "functionplan" {
  name                = "function-app-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1"
  tags               = {
    Environment = var.environment
  }
}

resource "azurerm_linux_function_app" "functionapp" {
  name                        = var.function_app_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  service_plan_id             = azurerm_service_plan.functionplan.id
  storage_account_name        = var.storage_account_name
  storage_account_access_key  = var.storage_account_access_key
  functions_extension_version = "~4"
  site_config {
    application_stack {
      python_version = "3.10"
    }
  }
  identity {
    type = "SystemAssigned"
  }
  tags               = {
    Environment = var.environment
  }
}
