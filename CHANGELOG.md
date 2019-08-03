# Release History

## 0.1.0 (2019-08-03)

**Added**

- init project with poetry, travis, pytest, coverage and coveralls
- feat: define each api in subclass of `BaseApi`
- feat: define each testcase in function startswith `test_`
- feat: prepare request, include params, headers, cookies, data/json
- feat: make request with requests.request
- feat: extract response status_code, headers field, field in json body
- feat: assert equivalence for extracted field with expected value
- feat: share public parameters in multiple apis of testcase
- feat: parameters correlation in single testcase
- feat: session sharing in single testcase
