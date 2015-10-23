require 'http'
require 'json'
require 'uri'

module TestExecsService
  class FromServer < Base
    @server_address = URI::HTTP.build({
      :host => 'localhost',
      :port => ENV[SIS_TEST_SERVER_PORT_ENV]
    }).to_s

    def self.get(uuid)
      status_request = URI.join(@server_address, 'status/', uuid.to_s)
      response = HTTP.get status_request
      if response.status_code >= 300
        return nil
      end
      JSON.parse response.body.to_s
    end

    def self.all_uuids
      JSON.parse HTTP.get(@server_address).body.to_s
    end
  end
end