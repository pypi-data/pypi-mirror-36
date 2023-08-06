# Python Modules for Selenium UnitTest

### Installation
```bash
pip install selenium-unittest-common
```

### Usage
```python
from selenium-unittest-common import test_case

class SampleTestCase(test_case.BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(SampleTestCase, cls).setUpClass()
        cls.base_url = 'https://www.google.com'
        cls.page_url = cls.base_url

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    def setUp(self):
        super(SampleTestCase, self).setUp()
        self.driver.get(self.page_url)
```

### Build & Pylint
1. Make sure below modules are installed:
* invoke
* pylint

2. Execute the following command
```
invoke clean build
```bash

### Docker

#### Launching Container
```bash
docker-compose up -d --build
```

#### Executing Python Script
```bash
docker exec -it python python /root/script/sample.py
```

### TODO
* Add support for FireFox. 
