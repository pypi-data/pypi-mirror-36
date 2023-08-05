# python-utopian-rocks
An API Wrapper for utopian.rocks.




## Installing

```cmd
pip install python_utopian_rocks
```

## Usage

```python

from python_utopian_rocks.client import Client

client = Client()
```


## Run  tests:

```cmd
python tests.py
```

## API

### Request method aliases

``client.get_posts(params)``

``client.get_moderators()``

``client.is_moderator(param)``

``client.get_moderators_by_category(params)``

``client.get_moderators_stats_by_category(params)``

``client.get_projects_stats_by_category(params)``

``client.get_contributors(param)``

``client.get_moderators_by_date(param)``

``client.get_categories_by_date(param)``

``client.get_projects_by_date(param)``

``client.get_staff_picks_by_date(param)``

``client.get_tasks_requests_by_date(param)``


### Request parameters

These are the available parameters for making requests.

In order to get posts :

```python
client.get_posts(category="<value>", status="<value>", author="<value>", moderator="<value>", staff_picks="<value>")
```
or
```python

client.get_posts({"category":"<value>","author":"<value>"})
```






For retriving all moderators:

```python
client.get_moderators()
```




For Statistics

```python
params = {"category":"<value>","author":"<value>"}
client.get_contributors(params);
```
 * You can use a specific date like 2020-06-24 or today, weekly.
```python

client.get_staff_picks_by_date(specificDate);
```


`

## Supported Tags

the following table is the correct values  for category ``parameter``

Tag | Task tag
--|--
development | task-development
copywriting | task-copywriting
graphics | task-graphics
analysis | task-analysis
social | task-social




## Contributing

Feel free to create any [pull requests](https://github.com/yucealiosman/python-utopian-rocks/compare).

## Bugs

If there is any bug please report it by opening a [new issue](https://github.com/yucealiosman/python-utopian-rocks/compare/issues/new).