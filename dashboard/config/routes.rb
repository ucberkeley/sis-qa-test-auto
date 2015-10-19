Rails.application.routes.draw do
  root 'test_execs#index'

  resources :text_execs, :only => [:index, :create, :new, :show, :destroy]
end
