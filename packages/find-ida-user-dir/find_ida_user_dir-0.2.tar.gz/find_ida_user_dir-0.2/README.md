`find_ida_user_dir` determines the current user's IDA Pro user directory in a platform independent way.

```python
import find_ida_user_dir
user_dir = find_ida_user_dir.find_path()

plugins_dir = find_ida_user_dir.find_path("plugins")
```

`find_ida_user_dir` first checks for the existence of an `IDAUSR` environment variable: if it is present, that is returned. If not, the correct path of the default user directory as described in the [IDA Pro documentation](https://www.hex-rays.com/products/ida/support/idadoc/1375.shtml) is returned. If a subdirectory name is given then the path to that subdirectory in the IDA user directory is returned.

`find_ida_user_dir` is useful for creating installation scripts for IDA plugins which need to identify the IDA user directory so that they know where to copy the plugin module to.