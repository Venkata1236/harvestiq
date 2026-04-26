# Training Notes

## Run Environment
- Train on: Google Colab (T4 GPU)
- Estimated time: ~2 hours

## Progressive Unfreezing Schedule
- Epochs 1-5:  Only FC head trains (lr=1e-4)
- Epochs 6-10: layer4 unfrozen (lr=1e-5)
- Epochs 11-15: layer3 unfrozen (lr=1e-6)

## Success Criteria
- Val accuracy > 88% → proceed
- Val accuracy < 88% → unfreeze layer2 and train 5 more epochs

## Colab Setup
```python
!git clone https://github.com/Venkata1236/harvestiq.git
%cd harvestiq/backend
!pip install torch torchvision loguru scikit-learn matplotlib seaborn
!kaggle datasets download -d vipoooool/new-plant-diseases-dataset
!unzip new-plant-diseases-dataset.zip -d data/
!python app/ml/train.py
```