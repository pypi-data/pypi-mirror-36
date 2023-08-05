# pinkboto

A Colorful AWS SDK wrapper for Python

## Install
    pip install pinkboto

## Usage
    import pinkboto
    aws = pinkboto.aws(profile='production', region='us-east-1') 
    selector = {'resource': 'aws_db_instance'}
    projection = ['DBInstanceIdentifier', 'Endpoint']
    rds = aws.find(selector, projection)

## Contributing
Pull requests for new features, bug fixes, and suggestions are welcome!

## License
GNU General Public License v3 (GPLv3)

