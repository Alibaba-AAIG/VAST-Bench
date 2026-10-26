require 'openssl'
module Railsguard
  class Middleware
    def initialize(app, secret:)
      @app, @secret = app, secret
    end
    def call(env)
      raw=env.fetch('HTTP_COOKIE','').split(';').map(&:strip).find { |x| x.start_with?('session=') }
      return [401,{},['missing signed session']] unless raw
      value, signature=raw.sub('session=','').split('--',2)
      expected=OpenSSL::HMAC.hexdigest('SHA256',@secret,value)
      valid=signature && signature.bytesize==expected.bytesize && OpenSSL.fixed_length_secure_compare(signature,expected)
      valid ? @app.call(env) : [401,{},['invalid signed session']]
    end
  end
end
