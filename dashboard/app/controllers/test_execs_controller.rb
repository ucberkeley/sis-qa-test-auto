class TestExecsController < ApplicationController
  @@test_execs_service = TestExecsService::FromServerCached

  def create
    render json: @@test_execs_service.execute
  end

  def index
    @num = params.fetch(:num, 0).to_i
    render json: @@test_execs_service.status_last(@num)
  end

  def show
    render json: @@test_execs_service.status(params[:id])
  end

  def delete
    puts '#delete not implemented'
    render json: @@test_execs_service.status(params[:id])
  end
end

