# aamporterpkg
## About
[aamporter](https://github.com/timsutton/aamporter) is a great tool. Unfortunately, it lacks the ability to convert downloaded adobe updates to pkgs, making it less useful for some deployment solutions.

aamporterpkg generates a pkg file and uses a simple shell script to mount and execute the contained adobe installer.

## Usage
aampkgporter can be used on it's own: ```./aamporterpkg pathToAdobeUpdate.dmg```

But it is probably more useful in combination with aamporter. The following command runs a aamporter plist and creates pkg files for every dmg that has been downloaded:
```/path/to/aamporter.py SomeAdobeProduct.plist && /path/to/aamporterpkg.py /path/to/aamportercache/*.dmg```
