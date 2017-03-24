# fbones
A bootstrap toolkit to kickoff a flask project

## install
    $sudo pip install fbones

## start a project

###1. create folder your self

    $mkdir myproject

###2. init project

    $cd myproject
    $fbones init
    
   This command will create folders and files project needed

###3. add blueprint

    $fbones addnp name

###4. echo supervisord conf

    $fbones deploy_supervisor [name] [port] [number of core]

  this command will just print on screen, use > to save a file:

    $fbones deploy_supervisor my_app 8000 4 > /etc/supervisord.d/my_app.conf

###5. echo nginx conf

    $fbones deploy_nginx [name] [upstream port] [domain]

  this command will print conf file on screen

    $fbones deploy_nginx my_app 80000 test.mydomain.com > /etc/nginx/conf.d/my_app.conf

###6. Generate service class from model class

    $fbones gen_serv models:User

  this command will print service class code from models.py





