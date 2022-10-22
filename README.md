# Normal Map Generation for Pixel Art
Paper: Analysis and Compilation of }Normal Map Generation Techniques for Pixel Art

Authors:
- Rodrigo D. Moreira
- Flávio Coutinho
- Luiz Chaimowicz

## Dependencies
`pip install -r requirements.txt`

## Run examples
Sobel from color map technique: `python albedo_generator.py`

Sobel from height map technique: `python heightmap_generator.py`

Bevel technique: `python bevel_generator.py`

Merge of four illumination angles technique: `python multiangle_generator.py`

## Using other images
Change parameters for the intended technique in the files above:
```python
  __init__(
    folder='path/to/image/folder',
    img_file='image_file.extension',
    normal_file_suffix='_suffix_for_output'
  )
```
