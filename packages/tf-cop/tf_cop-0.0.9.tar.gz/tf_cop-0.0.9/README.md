# Terraform automatic reviewer

terraform scripts checker.<br>
This package helps you to review your tf script.<br>
(ex: confirm add logging rule to all s3 bucket)


## Installation

```bash
$ pip install tf_cop
```


## Usage
#### do review
pass `terraform root path` & `review_book root path`

```python
import tf_cop

if __name__ == '__main__':
    test = tf_cop.TfCop()
    test.tf_review("./test", "./review_book_default")
```

#### get output

```python
    output = test.output(color_flg=True)
    print(output["output_log"])
    print(output["output_summary_log"])
    print(output["program_error_log"])
    print(output["system_log"])
```

## Review_book yaml rule

|key  |description  |required|
|---|---|---|
|title  |test title|required|
|desc  |description for test|option|
|mode|test mode (existance\|value\|nested)|required|
|key|test target key (ex. tags)|required|
|value|correct value regex|option|
|nest|for nested test|option|
|warn|for warn message|option (default False)|

### existance test
check if target key is exist.<br>
(ex. description)

### value test
check if target value is correct.<br>
(ex. name = "(prd|stg|dev)-s3-.*-terraform")

### nested test
test to nested key_value
```hcl
tags {
    Name = "${terraform.env}-tf-review-bucket"
    Env = "dev"
}
```

## Testing
`python test.py`

## Sample usage
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
    print(output["output_log"])
    print(output["output_summary_log"])
    print(output["program_error_log"])
```

set `TF_ROOT_PATH` & `REVIEW_BOOK_PATH`

```bash
docker build -t tf_cop .
docker run \
      -v `pwd`/${TF_ROOT_PATH}:/tmp/terraform \
      -v `pwd`/${REVIEW_BOOK_PATH}:/tmp/review_book \
      tf_cop
```

## Author
ys-tydy
