variable "location" {
  type    = string
  default = "West Europe"
}

variable "resource_group_name" {
  type    = string
  default = "BeStrong-AI"
}

variable "storage_account_name" {
  type    = string
  default = "ocrdocaistorage"
}

variable "function_app_name" {
  type    = string
  default = "ocr-docai-function"
}

variable "subscription_id" {
  type      = string
  sensitive = true
}

variable "account_tier_terraform_state" {
  description = "Azure Storage Account and Private Endpoint for File Share account tier"
  type        = string
  default     = "Standard"
}

variable "account_replication_type_terraform_state" {
  description = "Azure Storage Account and Private Endpoint for File Share account replication type"
  type        = string
  default     = "LRS"
}