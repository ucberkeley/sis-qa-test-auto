class TestExec
  attr_reader :uuid, :status, :counters

  def initialize(uuid, status, counters={}, steps={})
    @uuid = uuid
    @status = status
    @counters = counters
    @steps = steps
  end
end
