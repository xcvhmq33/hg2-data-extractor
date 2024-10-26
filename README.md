# About
hg2-data-extractor is a Python package for downloading, decrypting and extracting [Houkai Gakuen 2](https://houkai2nd.miraheze.org/wiki/Houkai_Gakuen_2_Wiki) unity text assets data

## Installation
```shell
pip install hg2-data-extractor
```

## Usage
To get help, type `--help` with any command or even package

### Download
To download data_all file use:

```shell
hg2-data-extractor download
```
By default, download directory is `./data_all/`

### Decrypt
To decrypt downloaded data_all file use:

```shell
hg2-data-extractor decrypt 
```
By default, decrypts `./data_all/data_all_encrypted.unity3d`

### Extract
To extract text assets data from data_all_decrypted use:

```shell
hg2-data-extractor extract --asset-names asset_name1,asset_name2,...
```
By default, `WeaponDataV3`, `CostumeDataV2`, `PassiveSkillDataV3`, `SpecialAttributeDataV2`, `PetData`, `PetSkillData` assets will be extracted to `./extracted/`  
To show all valid asset names, use (data_all_decrypted is required):

```shell
hg2-data-extractor lst
```

# Credits
This project is a copied and modified version of [hg2-downloader](https://dev.s-ul.net/BLUEALiCE/hg2-downloader) project authored by [BLUEALiCE](https://dev.s-ul.net/BLUEALiCE)