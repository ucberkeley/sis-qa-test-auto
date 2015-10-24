module TestExecsService
  class FromServerCached < FromServer
    @cache = {}

    def self.execute
      uuid = FromServer.execute
      unless uuid.nil?
        self.status uuid
      end
    end

    def self.status(uuid)
      test_exec = FromServer.status uuid
      @cache[uuid] = test_exec
    end

    def self.status_last(n=nil)
      if n.nil?
        n = @cache.size
      end

      @cache.keys.sort!.reverse!.last(n).map do |uuid|
        self.status uuid
      end
    end

    def self.all_uuids
      @cache.keys
    end
  end
end