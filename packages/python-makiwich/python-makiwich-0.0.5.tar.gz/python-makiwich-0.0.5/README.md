# python-makiwich

- python port of https://github.com/mapbox/makiwich
- Uses CC0 [Maki icons](https://github.com/mapbox/maki/)
- Dependencies: [xmltodict](https://pypi.org/project/xmltodict/), for PNG export: [cairosvg](https://pypi.org/project/CairoSVG/)
- Contains Django view to serve icons in `maki.contrib.django.maki_icon`

The icons are not included in this repository, so building the package requires downloading the [Maki icons](https://www.mapbox.com/maki-icons/):

```
curl -L https://github.com/mapbox/maki/archive/master.zip -o maki-master.zip
unzip -qj maki-master.zip 'maki-master/icons/*' -d maki/img/icons/
```

# usage

```python
>>> from maki import MakiMarker
>>> marker = MakiMarker(symbol="park", tint="#3388ff")
>>> marker.svg()
'<?xml version="1.0" encoding="utf-8"?>\n<svg width="27px" height="41px" viewBox="0 0 27 41" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><desc>Created with Sketch.</desc><defs></defs><g id="marker-large" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g id="Page-1" fill-rule="nonzero"><g id="shadow" transform="translate(3.000000, 29.000000)" fill="#000000"><ellipse id="ellipse9048" opacity="0.04" cx="10.5" cy="5.80029008" rx="10.5" ry="5.25002273"></ellipse><ellipse id="ellipse8490" opacity="0.04" cx="10.5" cy="5.80029008" rx="10.5" ry="5.25002273"></ellipse><ellipse id="ellipse8492" opacity="0.04" cx="10.5" cy="5.80029008" rx="9.5" ry="4.77275007"></ellipse><ellipse id="ellipse8494" opacity="0.04" cx="10.5" cy="5.80029008" rx="8.5" ry="4.29549936"></ellipse><ellipse id="ellipse8496" opacity="0.04" cx="10.5" cy="5.80029008" rx="7.5" ry="3.81822308"></ellipse><ellipse id="ellipse8498" opacity="0.04" cx="10.5" cy="5.80029008" rx="6.5" ry="3.34094679"></ellipse><ellipse id="ellipse8500" opacity="0.04" cx="10.5" cy="5.80029008" rx="5.5" ry="2.86367051"></ellipse><ellipse id="ellipse8502" opacity="0.04" cx="10.5" cy="5.80029008" rx="4.5" ry="2.38636864"></ellipse></g><g id="background" fill="#3388FF"><path d="M27,13.5 C27,19.074644 20.250001,27.000002 14.75,34.500002 C14.016665,35.500004 12.983335,35.500004 12.25,34.500002 C6.7499993,27.000002 0,19.222562 0,13.5 C0,6.0441559 6.0441559,0 13.5,0 C20.955844,0 27,6.0441559 27,13.5 Z" id="path12645"></path></g><g id="border" opacity="0.25" fill="#000000"><path d="M13.5,0 C6.0441559,0 0,6.0441559 0,13.5 C0,19.222562 6.7499993,27 12.25,34.5 C13,35.522727 14.016664,35.500004 14.75,34.5 C20.250001,27 27,19.074644 27,13.5 C27,6.0441559 20.955844,0 13.5,0 Z M13.5,1 C20.415404,1 26,6.584596 26,13.5 C26,15.898657 24.495584,19.181431 22.220703,22.738281 C19.945823,26.295132 16.705119,30.142167 13.943359,33.908203 C13.743445,34.180814 13.612715,34.322738 13.5,34.441406 C13.387285,34.322738 13.256555,34.180814 13.056641,33.908203 C10.284481,30.127985 7.4148684,26.314159 5.015625,22.773438 C2.6163816,19.232715 1,15.953538 1,13.5 C1,6.584596 6.584596,1 13.5,1 Z" id="path12645-9"></path></g><g id="maki" transform="translate(6.000000, 7.000000)" fill="#FFFFFF"><path id="icon" d="M14,5.75c0.0113-0.6863-0.3798-1.3159-1-1.61C12.9475,3.4906,12.4014,2.9926,11.75,3  c-0.0988,0.0079-0.1962,0.0281-0.29,0.06c-0.0607-0.66-0.6449-1.1458-1.3048-1.0851C9.8965,1.9987,9.6526,2.1058,9.46,2.28l0,0  c0-0.6904-0.5596-1.25-1.25-1.25S6.96,1.5896,6.96,2.28C6.96,2.28,7,2.3,7,2.33C6.4886,1.8913,5.7184,1.9503,5.2797,2.4618  C5.1316,2.6345,5.0347,2.8451,5,3.07C4.8417,3.0195,4.6761,2.9959,4.51,3C3.6816,2.9931,3.0044,3.659,2.9975,4.4874  C2.9958,4.6872,3.0341,4.8852,3.11,5.07C2.3175,5.2915,1.8546,6.1136,2.0761,6.9061C2.2163,7.4078,2.6083,7.7998,3.11,7.94  c0.2533,0.7829,1.0934,1.2123,1.8763,0.959C5.5216,8.7258,5.9137,8.2659,6,7.71C6.183,7.8691,6.4093,7.9701,6.65,8v5L5,14h5l-1.6-1  v-2c0.7381-0.8915,1.6915-1.5799,2.77-2c0.8012,0.1879,1.603-0.3092,1.7909-1.1103C12.9893,7.7686,13.0025,7.6444,13,7.52  c0.0029-0.0533,0.0029-0.1067,0-0.16C13.6202,7.0659,14.0113,6.4363,14,5.75z M8.4,10.26V6.82C8.6703,7.3007,9.1785,7.5987,9.73,7.6  h0.28c0.0156,0.4391,0.2242,0.849,0.57,1.12C9.7643,9.094,9.0251,9.6162,8.4,10.26z" style="fill:#fff"></path></g></g></g></svg>'
```

# Known issues / TODO

- Letters / numbers not supported yet.
- Decide how to keep the icon files (currently not in the repo.)
- Error messages for missing icons need improvement
- check/extend/test `Color.most_readable` implementation
