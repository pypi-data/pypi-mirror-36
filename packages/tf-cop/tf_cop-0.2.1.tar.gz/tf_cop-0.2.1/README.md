# Terraform automatic reviewer

terraform scripts checker.<br>
This package helps you to review your tf script.<br>
(ex: confirm add logging rule to all s3 bucket)

## 1 Installation

```shell
$ pip install tf_cop
```


## 2 Usage
### 2.1 cli use
at your console

```shell
$ tfcop TERRAFORM_ROOT_PATH REVIEW_BOOK_ROOT_PATH(optional)
```

sample output

```shell
☁  tf_cop [master] ⚡ tfcop test
[INFO] tf_root_path     : test
[INFO] rbook_root_path  :

==========================================================
RESOURCE AWS_S3_BUCKET.TEST_TF_REVIEW_BUCKET
==========================================================
[WARN]  desc_checker    : description not use
[ALERT] tag_checker     : tags not use

==========================================================
RESOURCE AWS_S3_BUCKET.TEST_TF_REVIEW_BUCKET2
==========================================================
[WARN]  desc_checker    : description not use
[PASS]  tag_checker     : passed
[PASS]  name_checker    : passed
[PASS]  env_checker     : passed

==========================================================
DATA AWS_S3_BUCKET.TEST_DATA_TF_REVIEW_BUCKET
==========================================================
[PASS]  bucket_checker  : passed

 =======================
| RESOURCE NUM  : 3     |
| warn NUM      : 2     |
| alert NUM     : 1     |
| pass NUM      : 4     |
 =======================
```
### 2.2 module use
#### 2.2.1 do review
pass `terraform root path` & `review_book root path`

```python
import tf_cop

if __name__ == '__main__':
    test = tf_cop.TfCop()
    test.tf_review("./test", "./review_book_default")
```

#### 2.2.2 get output

```python
    output = test.output(color_flg=True)
    print(output)
```

## 3 Review_book yaml rule

### 3.1 file name rule

```python
review_book_yaml = resource_name.split("_")[1] + '.yaml'
```
(ex. aws_s3_bucket => s3.yaml)

folder structure
```
${REVIEW_BOOK_ROOT_PATH}
├── data
│   ├──s3.yaml
│   └──...
└── resource
    ├── acm.yaml
    ├── api.yaml
    └── ...
```

### 3.2 key rule

|key  |description  |required|
|---|---|---|
|title  |test title|required|
|desc  |description for test|option|
|mode|test mode (existance\|value\|nested)|required|
|key|test target key (ex. tags)|required|
|value|correct value regex|option|
|nest|for nested test|option|
|type|test type (ex. alert, warn)|required|

#### 3.2.1 existance test
check if target key is exist.<br>
(ex. description)

#### 3.2.2 value test
check if target value is correct.<br>
(ex. name = "(prd|stg|dev)-s3-.*-terraform")

#### 3.2.3 nested test
test to nested key_value
```hcl
tags {
    Name = "${terraform.env}-tf-review-bucket"
    Env = "dev"
}
```

### 3.3 sample
```yaml
aws_s3_bucket:
-
  title: description_checker
  description: simple existance checker
  mode: existance
  warn: True
  key: description
-
  title: private_checker
  description: simple value checker
  mode: value
  key: acl
  value: private
-
  title: bucket_checker
  description: simple value regex checker
  mode: value
  key: bucket
  value: .*-tf-review-bucket.*
-
  title: tag_checker
  description: nested value checker
  mode: nested
  key: tags
  nest:
    -
      title: name_checker
      description: nested value checker
      mode: value
      key: Name
      value: .*-tf-review-bucket.*
    -
      title: env_checker
      description: nested value checker
      mode: value
      warn: True
      key: Env
      value: (dev|stg|prd)
-
  title: if_checker
  mode: if
  key: logging
  nest:
    title: name_checker
    mode: existance
    key: lifecycle_rule
```

## 4 Testing
`python test.py`

## 5 Sample usage
test terraform files using docker.

```
├── Dockerfile
├── main.py
└── requirements.txt
```

```dockerfile
FROM python:3.6

RUN apt-get update
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /tmp

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python","main.py"]
```


```python
import tf_cop

if __name__ == '__main__':
    test = tf_cop.TfCop()
    test.tf_review("./terraform", "./review_book")

    output = test.output(color_flg=True)
    print(output)
```

set `TF_ROOT_PATH` & `REVIEW_BOOK_PATH`

```bash
docker build -t tf_cop .
docker run \
      -v `pwd`/${TF_ROOT_PATH}:/tmp/terraform \
      -v `pwd`/${REVIEW_BOOK_PATH}:/tmp/review_book \
      tf_cop
```

## 6 Author
ys-tydy
