from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="XDD_K8S_CERTS",
    settings_files=["settings.toml", ".dev_secrets.toml"],
    environments=True,
    default_env="production",
    env_switcher="XDD_K8S_CERTS_ENVIRONMENT",
)

# settings.validators.register(
#    Validator('spreadsheet_id', must_exist=True),
#    Validator('service_account_file_path', must_exist=True, env='development'),
# )
# settings.validators.validate()
