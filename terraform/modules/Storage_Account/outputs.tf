output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "storage_account_access_key" {
  value = azurerm_storage_account.main.primary_access_key
}