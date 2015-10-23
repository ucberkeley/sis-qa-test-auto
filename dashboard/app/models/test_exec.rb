class TestExec
  attr_reader :uuid, :status, :counters

  def initialize(uuid, status, counters={})
    @uuid = uuid
    @status = status
    @counters = counters
  end
end
