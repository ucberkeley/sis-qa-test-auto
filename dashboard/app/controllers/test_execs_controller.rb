class TestExecsController < ApplicationController
  def create
    redirect_to test_execs_url
  end

  def show
    @test_exec = TestExecsService::FromServerCached.get(params[:id])
  end
  
  private
    def test_exec_params
      params.require(:test_exec).permit(:name)
    end
end

