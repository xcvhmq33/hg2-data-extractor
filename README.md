# About
hg2-data-extractor is a Python package for downloading, decrypting and extracting [Houkai Gakuen 2](https://houkai2nd.miraheze.org/wiki/Houkai_Gakuen_2_Wiki) unity text assets data

## Installation
### From PyPi
```shell
pip install hg2-data-extractor
```

## Usage
To get help, type `--help` with any command or even package

### Download
To download data_all file use:

```shell
hg2-data-extractor download server version              # Downloads to ./data_all/
hg2-data-extractor download server version path/to/dir  # Downloads to path/to/dir
```
Where **server** must be `JP` or `CN` and **version** must be a valid game version (e.g `11_1` or `9.8`)

### Decrypt
To decrypt downloaded data_all file use:

```shell
hg2-data-extractor decrypt                                              # Decrypts ./data_all/data_all.unity3d to ./data_all/data_all_dec.unity3d
hg2-data-extractor decrypt path/to/file.unity3d                         # Decrypts file.unity3d to ./data_all/data_all_dec.unity3d
hg2-data-extractor decrypt path/to/file1.unity3d path/to/file2.unity3d  # Decrypts file1.unity3d to file2.unity3d
```

### Extract
To extract text assets data from data_all_dec use:

```shell
hg2-data-extractor extract                                                                  # Extracts all ItemData assets from ./data_all/data_all_dec.unity3d to ./extracted/
hg2-data-extractor extract AssetName1,AssetName2                                            # Extracts AssetName1,AssetName2 from ./data_all/data_all_dec.unity3d to ./extracted/
hg2-data-extractor extract AssetName1,AssetName2 path/to/dir                                # Extracts AssetName1,AssetName2 from ./data_all/data_all_dec.unity3d to path/to/dir
hg2-data-extractor extract AssetName1,AssetName2 path/to/dir path/to/data_all_dec.unity3d   # Extracts AssetName1,AssetName2 from data_all_dec.unity3d to path/to/dir
```

### List
To create file with all valid asset names in data_all_dec use:

```shell
hg2-data-extractor lst                                                # Writes from ./data_all/data_all_dec.unity3d to ./extracted/asset_names.txt
hg2-data-extractor lst path/to/file.txt                               # Writes from ./data_all/data_all_dec.unity3d to file.txt
hg2-data-extractor lst path/to/file.txt path/to/data_all_dec.unity3d  # Writes from data_all_dec.unity3d to file.txt
```

# Credits
This project is a copied and modified version of [hg2-downloader](https://dev.s-ul.net/BLUEALiCE/hg2-downloader) project authored by [BLUEALiCE](https://dev.s-ul.net/BLUEALiCE)