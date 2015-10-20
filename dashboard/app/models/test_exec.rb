class TestExec < ActiveRecord::Base
  # TODO: Extract enum into configuration file. Currently, this enum
  #   is a copy of TestsExecStatusEnum in server/src/executor.py
  enum status: {errored: -1, done: 0, queued: 1, dryrun: 2, executing: 3}
end
