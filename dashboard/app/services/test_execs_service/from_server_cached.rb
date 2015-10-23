module TestExecsService
  class FromServerCached < FromServer
    @cache = {}

    def self.get(uuid)
      unless @cache.has_key? uuid
        @cache[uuid] = FromServer.get uuid
      end

      @cache[uuid]
    end
  end
end