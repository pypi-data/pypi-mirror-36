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

```
    ptint(test.result())
    ptint(test.result_summary())
    ptint(test.program_error_log())
```

## Review_book yaml rule

## Testing

## Author
ys-tydy
