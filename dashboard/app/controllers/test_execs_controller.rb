class TestExecsController < ApplicationController
  def create
    render plain: params[:test_exec].inspect
  end
end
