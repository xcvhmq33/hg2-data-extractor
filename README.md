# **About**
hg2-data-extractor is a Python package for downloading, decrypting, and extracting [Houkai Gakuen 2](https://houkai2nd.miraheze.org/wiki/Houkai_Gakuen_2_Wiki) Unity text asset data.

## **Installation**
### **From PyPi**
```bash
pip install hg2-data-extractor
```

## **Commands Overview**

The CLI offers several commands for processing data. Below is a quick summary:

| Command        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `lst`          | Prints a list of all available asset names.                                 |
| `download`     | Downloads the `data_all.unity3d` file from a server.                        |
| `decrypt`      | Decrypts the `data_all.unity3d` file into a ready-to-extract format.        |
| `extract`      | Extracts specific assets or a preset of assets into `.tsv` files.           |
| `resources`    | Downloads resource files from a server (e.g., auido.pck, video.mp4).        |

---

## **Usage**

The CLI is invoked through a main entry point (e.g., `hg2-data-extractor` or `python -m <module-name>`). Below are detailed examples for each command.

### **1. List Available Assets**
Prints a list of all assets from the decrypted `data_all.unity3d` file.

```bash
hg2-data-extractor lst --output-dir extracted --data-all path/to/data_all_dec.unity3d
```

| Option       | Description                                      | Default Value                        |
|--------------|--------------------------------------------------|--------------------------------------|
| `--output-dir`, `-o`  | Directory to save the output file.      | `extracted`                          |
| `--data-all`, `-d`    | Path to the decrypted `data_all` file.  | `data_all/data_all_dec.unity3d`      |

---

### **2. Download Data**
Downloads the `data_all.unity3d` file from the specified server.

```bash
hg2-data-extractor download <server> <version> --decrypt --output-dir extracted
```

| Option        | Description                                           | Default Value     |
|---------------|-------------------------------------------------------|-------------------|
| `<server>`    | The server to download from (`CN`, `JP`).             | *Required*        |
| `<version>`   | The version of the game (e.g., `11.1` or `9_8`).      | *Required*        |
| `--decrypt`   | Decrypts the downloaded file.                         | `False`           |
| `--output-dir`, `-o` | Directory to save the downloaded file.         | `extracted`       |

---

### **3. Decrypt Data**
Decrypts an encrypted `data_all.unity3d` file.

```bash
hg2-data-extractor decrypt <input> --output-dir data_all
```

| Option               | Description                                  | Default Value              |
|----------------------|----------------------------------------------|----------------------------|
| `<input>`            | Path to the file to decrypt.                 | `data_all/data_all.unity3d`|
| `--output-dir`, `-o` | Directory to save the decrypted file.        | `data_all`                 |

---

### **4. Extract Assets**
Extracts specific assets or a preset of assets into `.tsv` files.

```bash
hg2-data-extractor extract <asset-names> --preset items --asset-file assets.txt --output-dir extracted --data-all path/to/data_all_dec.unity3d
```

| Option                | Description                                             | Default Value                    |
|-----------------------|---------------------------------------------------------|----------------------------------|
| `<asset-names>`       | Names of assets to extract.                             | `None`                           |
| `--preset`, `-p`      | Preset of assets to extract (`items`, `story`).         | `None`                           |
| `--asset-file`, `-f`  | Path to a file with line-separated asset names.         | `None`                           |
| `--output-dir`, `-o`  | Directory to save the extracted files.                  | `extracted`                      |
| `--data-all`, `-d`    | Path to the decrypted `data_all` file.                  | `data_all/data_all_dec.unity3d`  |

---

### **5. Download Resources**
Downloads resource files from a server (e.g., auido.pck, video.mp4).

```bash
hg2-data-extractor resources <server> <version> --overwrite --output-dir resources
```

| Option        | Description                                           | Default Value     |
|---------------|-------------------------------------------------------|-------------------|
| `<server>`    | The server to download from (`CN`, `JP`).             | *Required*        |
| `<version>`   | The version of the game (e.g., `11.1` or `9_8`).      | *Required*        |
| `--overwrite` | Overwrites existing files.                            | `False`           |
| `--output-dir`, `-o` | Directory to save the downloaded file.         | `resources`       |

---

## **Examples**

### **1. Download, Decrypt, and Extract Preset**
Download data from the JP server for version `11.1`, decrypt it, and extract items:

```bash
hg2-data-extractor download JP 11.1 --decrypt --output-dir extracted
hg2-data-extractor extract --preset items --data-all extracted/data_all_dec.unity3d --output-dir extracted
```

### **2. Extract Specific Assets**
Extract specific assets by name:

```bash
hg2-data-extractor extract WeaponDataV3 PassiveSkillDataV3 --data-all data_all/data_all_dec.unity3d --output-dir assets
```

### **3. Use a File for Asset Names**
Extract assets listed in a file:

```bash
hg2-data-extractor extract --asset-file assets.txt --data-all data_all/data_all_dec.unity3d --output-dir assets
```

# Credits
This project is a modified version of the [hg2-downloader](https://dev.s-ul.net/BLUEALiCE/hg2-downloader) project by [BLUEALiCE](https://dev.s-ul.net/BLUEALiCE)