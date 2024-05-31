terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}


resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("~/.ssh/id_rsa.pub") # Path to your public key
}



resource "aws_instance" "django_instance" {
  ami             = "ami-08188dffd130a1ac2" # Amazon Linux 2023 AMI
  instance_type   = "t2.micro"
  key_name        = aws_key_pair.deployer.key_name
  subnet_id       = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.server.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y git python3.11 python3.11-pip nginx
              curl -sSL https://install.python-poetry.org | python3.11 -
              git clone https://github.com/honcharevskiy/charity.git /home/ec2-user/django
              cd /home/ec2-user/django
              poetry env use /usr/bin/python3.11
              poetry install --no-interaction --no-ansi --no-root
              poetry run python manage.py migrate
              poetry run python manage.py collectstatic --noinput

              # Install Gunicorn
              pip3 install gunicorn

              # Create a systemd service file for Gunicorn
              cat > /etc/systemd/system/gunicorn.service <<EOL
              [Unit]
              Description=gunicorn daemon
              After=network.target

              [Service]
              User=ec2-user
              Group=nginx
              WorkingDirectory=/home/ec2-user/django
              ExecStart=/home/ec2-user/.local/bin/poetry run gunicorn --access-logfile - --workers 3 --bind unix:/home/ec2-user/django.sock charity.wsgi:application

              [Install]
              WantedBy=multi-user.target
              EOL

              # Start and enable Gunicorn
              sudo systemctl start gunicorn
              sudo systemctl enable gunicorn

              # Configure Nginx
              cat > /etc/nginx/nginx.conf <<EOL
              user ec2-user;
              worker_processes auto;
              error_log /var/log/nginx/error.log;
              pid /run/nginx.pid;

              events {
                  worker_connections 1024;
              }

              http {
                  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                                    '$status $body_bytes_sent "$http_referer" '
                                    '"$http_user_agent" "$http_x_forwarded_for"';

                  access_log  /var/log/nginx/access.log  main;

                  sendfile            on;
                  tcp_nopush          on;
                  tcp_nodelay         on;
                  keepalive_timeout   65;
                  types_hash_max_size 2048;

                  include             /etc/nginx/mime.types;
                  default_type        application/octet-stream;

                  include /etc/nginx/conf.d/*.conf;

                  server {
                      listen 80;
                      server_name _;

                      location / {
                          proxy_pass http://unix:/home/ec2-user/django.sock;
                          proxy_set_header Host $host;
                          proxy_set_header X-Real-IP $remote_addr;
                          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                          proxy_set_header X-Forwarded-Proto $scheme;
                      }

                      location /staticfiles/ {
                          alias /home/ec2-user/django/static/;
                      }

                      location /mediafiles/ {
                          alias /home/ec2-user/django/mediafiles/;
                      }
                  }
              }
              EOL

              sudo systemctl restart nginx
              sudo systemctl enable nginx
              EOF

  tags = {
    Name = "Charity"
  }
}
