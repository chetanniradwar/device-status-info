
## Project Setup for Mac

1. install brew using `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2. install pipenv globally using `brew install pipenv`

3. install redis using `brew install redis`

4. create a project folder `DeviceStatus`

5. clone the git repo locally using `https://github.com/chetanniradwar/device-status-info.git` in 'DeviceStatus' folder

6. in current folder run `pipenv shell` to create virtual environment

7. `pipenv install` to install all the project dependencies

8. then, `cd devicestatus` folder inside which `manage.py` file is there.

9. run `python manage.py migrate` to migrate all migrations and create table in the database

10. run the redis cache server locally using `redis-server` on default port `6379`

11. run `python manage.py runserver 8002` to run the development server on 8002 port


## Postman documentation link
- [postman doc link](https://documenter.getpostman.com/view/20803750/2s946k5q6e)

## Assumption Made
1. Redis is used for caching the requested data for a temporary time period, assumed value `DEFAULT_CACHE_TIMEOUT` = 1 hour
2. So if requested data in available in cache data will be returned from cache otherwise from the SQLite DB.
3. Made a separate API to dumping all the data from the CSV file to a RDBMS, then only other apis can be triggered
4. APIs details given in API doc link

## Technologies Used
- `pipenv` - for making virtual environment
- `django-redis` - for redis support in django
- `django` - full stack web framework in python


