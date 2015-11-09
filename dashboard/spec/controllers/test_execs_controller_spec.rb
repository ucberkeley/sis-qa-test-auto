require 'rails_helper'

RSpec.describe TestExecsController, :type => :controller do

  describe 'GET index' do
    it 'returns http success' do
      get :index
      expect(response).to have_http_status(:success)
    end
  end

  describe 'GET show' do
    it 'returns http success' do
      get :show, :id => 123456789
      expect(response).to have_http_status(:success)
    end
  end

  describe 'GET create' do
    it 'returns http success' do
      get :create
      expect(response).to redirect_to :test_execs
    end
  end

end
