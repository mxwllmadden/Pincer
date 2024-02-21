# Pincer
_A simple automated analysis framework for electrophysiology traces_

## Installation
Use the provided anaconda environment file.

### Step 1: Install Anaconda
Visit the official [Anaconda website](https://www.anaconda.com/download) to download the installer and follow all directions.

### Step 2: Create the Anaconda Environment
Open Anaconda Prompt and use the following commands.

To create environment for the first time

```
conda env create --file "absolute/path/to/environment.yml"
```

If you ever need to update the environment at a later time from the same environment file, use

```
conda activate Kookaburra
```
then
```
conda env update --file "absolute/path/to/environment.yml" --prune
```

### Step 3: Create an analysis script and celldex in your favorite IDE

Examples have been provided within the top level of the repository.
