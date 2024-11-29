
## Setting Up a Conda Environment for FLAVR

Follow the steps below to create a Conda environment for the FLAVR project.

### 1. Create a Conda Environment

Open your terminal and run the following command to create a new Conda environment named `flavrenv` with Python 3.10:

```bash
conda create -n flavrenv python=3.10
```

### 2. Activate the Conda Environment

Activate the newly created environment using the following command:

```bash
conda activate flavrenv
```

### 3. Install Packages

#### For CUDA (If you have a compatible GPU)

Run the following command to install PyTorch and related packages for CUDA support:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### For CPU (If you do not have a CUDA-enabled GPU)

Use the following command to install PyTorch and related packages for CPU:

```bash
pip install torch torchvision torchaudio
```

#### Additional Packages

Install the required additional packages:

```bash
pip install opencv-python
pip install tqdm
pip install av
```

### 4. Make it Portable (Optional)

To make the environment portable:

1. With `flavrenv` active, install `conda-pack`:

   ```bash
   conda install -y -c conda-forge conda-pack
   ```

2. Save the `flavrenv` environment as a `.zip`:

   ```bash
   conda-pack --format zip
   ```

## Training the FLAVR Model

### Training on Vimeo-90K Septuplets

For training your own model on the Vimeo-90K dataset, use the following command. You can download the dataset from [this link](http://toflow.csail.mit.edu/). The results reported in the paper are trained using 8 GPUs.

```bash
python main.py --batch_size 32 --test_batch_size 32 --dataset vimeo90K_septuplet --loss 1*L1 --max_epoch 200 --lr 0.0002 --data_root <dataset_path> --n_outputs 1
```

### Training on GoPro Dataset

Training on the GoPro dataset is similar, but for 8x interpolation, set `n_outputs` to 7.

```bash
python main.py --batch_size 32 --test_batch_size 32 --dataset gopro --loss 1*L1 --max_epoch 200 --lr 0.0002 --data_root <dataset_path> --n_outputs 7
```

## Testing Using Trained Model

### Pretrained Models

You can download the pretrained FLAVR models from the following links:

| Method     | Trained Model                                                         |
|------------|----------------------------------------------------------------------|
| **2x**     | [Link](https://drive.google.com/file/d/1IZe-39ZuXy3OheGJC-fT3shZocGYuNdH/view?usp=sharing) |
| **4x**     | [Link](https://drive.google.com/file/d/1GARJK0Ti1gLH_O0spxAEqzbMwUKqE37S/view?usp=sharing) |
| **8x**     | [Link](https://drive.google.com/file/d/1xoZqWJdIOjSaE2DtH4ifXKlRwFySm5Gq/view?usp=sharing) |

### 2x Interpolation

For testing a pretrained model on the Vimeo-90K septuplet validation set, run the following command:

```bash
python test.py --dataset vimeo90K_septuplet --data_root <data_path> --load_from <saved_model> --n_outputs 1
```

### 4x and 8x Interpolation

For testing a pretrained multiframe FLAVR model (using the GoPro dataset), adjust `n_outputs` to match the desired output (4x or 8x). Example for 8x interpolation:

```bash
python test.py --dataset gopro --data_root <data_path> --load_from <saved_model> --n_outputs 7
```

## Notes

- For **2x interpolation**, the Vimeo-90K dataset is used.
- For **4x and 8x interpolation**, use the GoPro dataset.