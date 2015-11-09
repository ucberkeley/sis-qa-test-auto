require 'pathname'

require 'sinatra/base'

class FakeTestExecsServer < Sinatra::Base
  get '/status/:uuid' do
    content_type :json
    status 200
    Pathname.new(__FILE__).dirname.join('fixtures').join('test_status.json').read
  end

  post '/execute' do
    '123456789'
  end
end
