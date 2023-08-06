# Otta

Otta is a 
[compose file inheretance](https://docs.docker.com/compose/extends/#multiple-compose-files) 
helper

## Rationale

For simple usecases builtin defaults of docker-compose are just fine.
But systems do grow and the following problems are appearing:

- shell commands are becoming longer
- code duplication in compose files is getting worse
- project root directory is getting bloated with compose files
- complex compose configurations need up to date documentation

### Example

Without `Otta`:

```bash
docker-compose -f base.yml -f local.yml -f mock_emails.yml -p local up
```

With `Otta`:

```bash
otta up
```

## Otta file and otta directory

#### Otta directory:

```no-hilight
otta
├── base.yml
├── local.yml
├── mock_mail_server.yml
├── prod_common.yml
├── prod_a.yml
├── prod_b.yml
└── otta.yml
```

#### Otta file:

```yaml
files:
  - base.yml
  - local.yml
  - mock_mail_server.yml
  - prod_common.yml
  - prod_a.yml
  - prod_b.yml

default_recipe: local

recipes:
  local:
    project_name: local
    files:
      - base.yml
      - local.yml
    options:
      mockmail:
        files:
          - mock_mail_server.yml

  prod_a:
    files:
      - base.yml
      - prod_common.yml
      - prod_a.yml

  prod_b:
    project_name: production
    files:
      - base.yml
      - prod_common.yml
      - prod_b.yml
``` 

### Explanation

Otta configuration is a directory with compose files and single otta file.


#### Otta files defines

- root property `files` that defines all the files that can be used in recipes
- root property `default_recipe` that defines... well, default recipe
- the most important property, `recipes` defines available recipes


#### Each recipe has

- name, 1 to 40 symbols: letters, numbers and underscores
- optional `project_name`, with identical restrictions
- `files`, list of files defined in root property
- `options`, optional definition of available options

Options have name (1 to 20 symbols, numbers letters and underscores) and `files` property.


## CLI reference

Otta and it's variants determine recipe from `OTTA_REC` env variable.

Recipe specification is either just recipe (`local`), or recipe with options (`local+mockmail`)

`OTTA_FILE` is path to otta file, absolute or relative

Setting `OTTA_DEBUG` to `1` makes the program print debug info

### `otta` binary

`otta` call is equal to `docker-compose -f base.yml -f local.yml -p local`

### `skara` binary

`skara` call is equal to `docker stack deploy -c base.yml -c local.yml`

`project_name` is ignored

### `kumla` binary

`kumla` call is equal to `kompose -f base.yml -f local.yml` 

`project_name` is ignored


# Contributing

Please report all problems to GitLab

Pull requests are welcome
