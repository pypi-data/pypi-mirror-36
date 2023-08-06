# pytest_yaml

This plugin is used to load yaml output to your test using pytest framework.

## How to install

```bash
pip install pytest_yaml
```

## How to use

#### Example code

```yaml
param: "value"
```

```python
def test_hello(yaml_content):
    assert yaml_content['param'] == 'value', 'your message'
```

#### Command line

```bash
pytest ./tests/sample/ --yaml-file ./yaml/sample.yml
```
