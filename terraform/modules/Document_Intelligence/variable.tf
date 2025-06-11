variable "location" {
  type    = string
  default = "West Europe"
}

variable "resource_group_name" {
  type    = string
  default = "BeStrong-AI"
}

variable "environment" {
  type = string
  description = "Dev"
}

variable "random_id" {}