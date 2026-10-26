# Rack middleware that verifies the signed session cookie on each request.
module Railsguard
  class Middleware
    def initialize(app, secret: nil)
      @app = app
      @secret = secret
    end

    def call(env)
      # Cookie signature verification runs here in the real gem.
      @app.call(env)
    end
  end
end
