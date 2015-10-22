require 'pathname'

class FromDisk < Base
  @test_logs_dir = ENV[SIS_TEST_DIR_ENV]

  def self.get(uuid)
    directory_path = Pathname.new(@test_logs_dir).join uuid
    unless directory_path.directory?
      return nil
    end

    json_hash = JSON.parse directory_path.join('result.json').read
    TestExec.new(uuid, json_hash['status'], json_hash['counters'])
  end

  def self.all_uuids
    Pathname.new(@test_logs_dir).each_entry.select(&:directory?).map do |p|
      p.basename.to_s
    end
  end
end