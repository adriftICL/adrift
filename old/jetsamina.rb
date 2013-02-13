require 'sinatra/base'

class MyApp < Sinatra::Base
  get '/' do
    haml :home
  end
  #get '/css/:name.scss' do |stylesheet|
  #  content_type 'text/css', :charset => 'utf-8'
  #  scss stylesheet
  #end
  run! if app_file == $0
end
