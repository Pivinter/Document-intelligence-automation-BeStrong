variable "location" {
  type    = string
  default = "West Europe"
}

variable "function_app_name" {
  type    = string
  default = "ocr-docai-function"
}

variable "resource_group_name" {
  type    = string
  default = "BeStrong-AI"
}

variable "storage_account_name" {
  type    = string
}

variable "storage_account_access_key" {
  type    = string
}

variable "environment" {
  type = string
  description = "Dev"
}