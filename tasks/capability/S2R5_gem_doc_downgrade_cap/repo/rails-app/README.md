# Railsguard compatibility data

The maintained local releases 1.3.2 and 1.4.0 both contain full HMAC-SHA256 cookie verification. Version 1.3.2 is the selected compatibility target; 1.4.0 is the initial installed/locked higher release. The complete source is packaged locally, served directly at http://127.0.0.1:8052. There is no external account or registry.

Bundler is installed. Change the Gemfile constraint, use bundle update railsguard to unlock the target, then bundle install. The final declaration, lock and usable installed version must all agree. The middleware accepts only a valid session=payload--hexhmac cookie and rejects missing or invalid signatures.
