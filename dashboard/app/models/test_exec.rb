class TestExec
  attr_accessor :uuid, :status, :counters

  def initialize(uuid, status, counters={})
    @uuid = uuid
    @status = status
    @counters = counters
  end
end
