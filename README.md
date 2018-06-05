# Github webhook to WooCommerce REST API

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org)

```sh
$ git clone git@github.com:landr-controlcode/github-woocommerce.git
$ cd github-woocommerce

$ pipenv install

$ createdb github-woocommerce

$ python manage.py migrate
$ python manage.py collectstatic

$ python manage.py runserver
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Documentation

- [WooCommerce REST API](http://woocommerce.github.io/woocommerce-rest-api-docs/).
- [Github webhook for release event](https://developer.github.com/v3/activity/events/types/#releaseevent)
- [Github REST API v3](https://developer.github.com/v3/repos/contents/) to get the contents of a release
