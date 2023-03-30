model_config_list {
  config {
    name: 'CashewClassification_model'
    base_path: '/CashewClassification_model/saved_models'
    model_platform: 'tensorflow'
    model_version_policy: {
	specific:{

		versions:  1
		versions:  2
		

		}
	}
  }
}