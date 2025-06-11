resource "azurerm_cognitive_account" "docai" {
  name                  = "docai-service"
  location              = var.location
  resource_group_name   = var.resource_group_name
  kind                  = "FormRecognizer"
  sku_name              = "S0"
  custom_subdomain_name = "docaiocr-${var.random_id}"
  tags               = {
    Environment = var.environment
  }
}