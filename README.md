# Number Conversion API

This API allows for the conversion of numerical values between binary (base 2), decimal (base 10), and hexadecimal (base 16) systems. It offers flexibility in handling inputs with or without prefixes and can return the results in a specified base or all three bases.

## Features
- Convert numbers between binary, decimal, and hexadecimal.
- Accept input numbers with or without 0b (binary) or 0x (hexadecimal) prefixes.
- Return conversions with or without prefixes based on the user's preference.
- Provide detailed error messages for incorrect inputs.

## Usage

### Endpoint

`GET /api`

### Parameters

- `from` (optional): The base of the input number. Can be `2` (binary), `10` (decimal), or `16` (hexadecimal). Defaults to `10` if not specified.
- `to` (optional): The base to convert the input number to. Can be `2` (binary), `10` (decimal), or `16` (hexadecimal). If not specified, the API returns the number in all three bases.
`value` (required): The number to be converted. Can include `0b` or `0x` prefix to indicate binary or hexadecimal, respectively. This prefix overrides the `from` parameter.
`prefix` (optional): Specify `true` to include prefixes (`0b` for binary, `0x` for hexadecimal) in the response. Default is `false`.

### Successful Response

`status`: `True`
`data`: An object containing the conversion results. The keys are the bases (`2`, `10`, `16`) and the values are the converted numbers in the respective bases.
`message`: "success"

### Error Response

`status`: `False`
`message`: An object containing an error `message` and a `hint`about how to correct the input.
`data`: An empty object.

## Examples

### Convert from Decimal to All Bases Without Prefix

Request:

```bash
GET /api?value=255
```

Response:

```json
{
    "status": true,
    "data": {
        "2": "11111111",
        "10": "255",
        "16": "ff"
    },
    "message": "success"
}
```

### Convert from Hexadecimal (with prefix) to Binary With Prefix

Request:

```bash
GET /api?value=0xff&prefix=true
```

Response:

```json
{
    "status": true,
    "data": {
        "2": "0b11111111",
        "10": "255",
        "16": "0xff"
    },
    "message": "success"
}
```

## Error Handling

### Request with invalid from value:

```sql
GET /api?from=3&value=255
```

Response:

```json
{
    "status": false,
    "message": {
        "message": "invalid arguments",
        "hint": "from parameter should be 2, 10, 16"
    },
    "data": {}
}
```

## Running the API

To run the API, ensure you have Flask installed in your environment. You can start the API server with the following command:

```
python app.py
```

This API is designed to be simple yet robust, providing clear feedback for any incorrect inputs to ensure users can easily correct their requests.