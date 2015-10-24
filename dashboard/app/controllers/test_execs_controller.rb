class TestExecsController < ApplicationController
  @@test_execs_service = TestExecsService::FromServerCached

  def create
    @test_exec = @@test_execs_service.execute
    redirect_to test_execs_url
  end

  def index
    @num = 5
    @test_execs = @@test_execs_service.status_last @num
  end

  def show
    @test_exec = @@test_execs_service.status params[:id]
  end
  
  private
    def test_exec_params
      params.require(:test_exec).permit(:name)
    end
end

