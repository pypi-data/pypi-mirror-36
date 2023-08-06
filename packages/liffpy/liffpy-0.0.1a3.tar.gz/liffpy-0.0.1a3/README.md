# liffpy
It is a package that allows you to manipulate LIFF(Line Frontend Framework) by Python.

# Caution

■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■
This branch is for `Alpha Version`.   
This package has little or no testing
□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□■□

# How to use

## Example

```python
# -*- coding:utf-8 -*-
from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)


def main():
    liff_api = LIFF("YOUR_CHANNEL_ACCESS_TOKEN")
    
    try:
        # If you want to add LIFF app
        liff_id = liff_api.add(
            view_type="compact",
            view_url="https://{YOUR LIFF-SITE}")
            # 400 Error or 401 Error
        try:
            # If you want to update LIFF app
            liff_api.update(liff_id, 
            view_type="full",
            view_url="https://{YOUR LIFF-SITE}")
        except ErrorResponse as err:
            # 401 Error or 404 Error
            print(err.message)
            return 
    except ErrorResponse as err:
        # 401 Error or 404 Error
        print(err.message)
        return 
    
    try:
        # If you want to get all LIFF apps
        apps_info = liff_api.get()
        for app_info in apps_info:
            try:
                # If you want to delete LIFF app
                liff_api.delete(app_info["liffId"])
            except ErrorResponse as err:
                # 401 Error or 404 Error
                print(err.message)
                return 
    except ErrorResponse as err:
        # 401 Error or 404 Error
        print(err.message)
        return 

if __name__ == '__main__':
    main()

```

## API

### LineFrontendFramework

#### `__init__(self, channel_access_token)`

Create a new LineFrontendFramework instance.

```python
liff_api = add(
            view_type="compact",
            view_url="https://{YOUR LIFF-SITE}")
```


#### `add(self, view_type, view_url)`

Adds an app to LIFF. You can add up to 30 LIFF apps on one channel.

```python
liff_id = LineFrontendFramework('YOUR_CHANNEL_ACCESS_TOKEN')
```

##### view_type

|name|mean|
|:---:|:---:|
|`"compact"`|50% of the screen height of the device|
|`"tall"`|80% of the screen height of the device.
|`"full"`|100% of the screen height of the device.|

"Add LIFF app" in [https://developers.line.me/ja/reference/liff/](https://developers.line.me/ja/reference/liff/)


#### `update(self, liff_id, view_type, view_url)`

Updates LIFF app settings.  

```python
liff_api.update(liff_id,
    view_type="full",
    view_url="https://{YOUR LIFF-SITE}")
```

##### view_type

|name|mean|
|:---:|:---:|
|`"compact"`|50% of the screen height of the device|
|`"tall"`|80% of the screen height of the device.
|`"full"`|100% of the screen height of the device.|

"Update LIFF app" in [https://developers.line.me/ja/reference/liff/](https://developers.line.me/ja/reference/liff/)

#### `get(self)`

Gets information on all the LIFF apps registered in the channel.

```python
liff_api.get()
```

"Get all LIFF apps" in [https://developers.line.me/ja/reference/liff/](https://developers.line.me/ja/reference/liff/)

#### `delete(self, liff_id)`

Deletes a LIFF app.

```python
liff_api.delete(liff_id)
```

"Delete LIFF app" in [https://developers.line.me/ja/reference/liff/](https://developers.line.me/ja/reference/liff/)
