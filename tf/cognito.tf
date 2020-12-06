resource "aws_cognito_user_pool" "djaphoto" {
  name = "djaphoto"

  account_recovery_setting {
    recovery_mechanism {
      name     = "admin_only"
      priority = 1
    }
  }
}


resource "aws_cognito_identity_provider" "google" {
  user_pool_id  = aws_cognito_user_pool.djaphoto.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    # From Google: https://console.developers.google.com/apis/credentials?project=djaphoto
    client_id     = var.google_client_id
    client_secret = var.google_client_secret

    # Automatically configured by Cognito
    attributes_url                = "https://people.googleapis.com/v1/people/me?personFields="
    attributes_url_add_attributes = true
    authorize_scopes              = "email openid profile"
    authorize_url                 = "https://accounts.google.com/o/oauth2/v2/auth"
    oidc_issuer                   = "https://accounts.google.com"
    token_request_method          = "POST"
    token_url                     = "https://www.googleapis.com/oauth2/v4/token"
  }

  attribute_mapping = {
    # `username` must be `sub`, this can(t be changed.
    # https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-specifying-attribute-mapping.html#cognito-user-pools-specifying-attribute-mapping-requirements
    username       = "sub"
    email          = "email"
    email_verified = "email_verified"
    family_name    = "family_name"
    gender         = "genders"
    locale         = "locale"
    given_name     = "given_name"
    name           = "name"
    picture        = "picture"

  }
}

resource "aws_cognito_user_pool_client" "backend" {
  name = "djaphoto-backend"

  generate_secret = true
  user_pool_id    = aws_cognito_user_pool.djaphoto.id

  callback_urls = [
    "http://localhost:8000/complete/cognito",
  ]

  logout_urls = [
    "http://localhost:8000/",
  ]

  allowed_oauth_scopes = [
    "openid",
    "profile",
    "email",
  ]

  allowed_oauth_flows = ["code"]


  allowed_oauth_flows_user_pool_client = true
  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
  ]
  supported_identity_providers = [
    "COGNITO",
    "Google"
  ]
}

resource "aws_cognito_user_pool_domain" "djaphoto" {
  domain       = "djaphoto"
  user_pool_id = aws_cognito_user_pool.djaphoto.id
}

output "client_id" {
  value = aws_cognito_user_pool_client.backend.id
}

output "client_secret" {
  value     = aws_cognito_user_pool_client.backend.client_secret
  sensitive = true
}
