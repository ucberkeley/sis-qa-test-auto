module TestExecsService
  class FromServerCached < FromServer
    @cache = {}

    def self.get(uuid)
      test_exec = FromServer.get uuid
      @cache[uuid] = test_exec
    end

    def self.get_last(n=nil)
      unless n
        n = @cache.size
      end

      @cache.keys.sort!.reverse!.last(n).map do |uuid|
        self.get uuid
      end
    end

    def self.all_uuids
      @cache.keys
    end
  end
end