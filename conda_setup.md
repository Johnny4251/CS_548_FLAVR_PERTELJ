# Setting Up a Conda Environment for FLAVR

Follow the steps below to create a Conda environment for the FLAVR project.

## Create a Conda Environment

Open your terminal and run the following command to create a new Conda environment named `flavrenv` with Python 3.10:

```bash
conda create -n flavrenv python=3.10
```

## Activate the Conda Environment

Activate the newly created environment using the following command:

```bash
conda activate flavrenv
```

## Install Packages

### For CUDA

If you have a compatible CUDA GPU, run the following command to install PyTorch and related packages:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### For CPU

If you do not have a CUDA-enabled GPU, use the following command to install PyTorch and related packages for CPU:

```bash
pip install torch torchvision torchaudio
```

### Additional Packages

Additional required packages

```bash
pip install opencv-python
pip install tqdm
pip install av
```

## Make it Portable (Optional)

### With `flavrenv` active, install `conda-pack`
```bash
conda install -y -c conda-forge conda-pack
```

### Save `flavrenv` environment as `.zip`
```bash
conda-pack --format zip
```