Rails.application.routes.draw do
  # root 'test_execs#index'

  # resources :test_execs, :only => [:index, :create, :new, :show, :destroy]

  root to: 'application#angular'

end
