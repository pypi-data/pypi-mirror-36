# tensorop
[![PyPI version](https://badge.fury.io/py/tensorop.svg)](https://badge.fury.io/py/tensorop) 

A Library which contains handy modules for convenience in Machine Learning and improved Kaggle support. Based on Pytorch. It's currently under development. Same API as Pytorch and Numpy. Main aim is to bring all functionalities that DL frameworks may lack for some reason but are essentially required for research/implementation purposes

## Installation
Installation via Pypi
```
$ pip install tensorop
```
Using with git
```
$ git clone https://github.com/prajjwal1/tensorop
$ cd tensorop
```

## Requirements
- Pytorch >= 0.4

## Components
- [tensor_func](#tensor_func)
- [np_utils](#np_utils)
- [optimizers](#optimizers)
- [loss_function](#Loss Function)
- [Kaggle](#kaggle)
- [Utilities](#utilities)

--------------------------------------------------------------------------------------------
### tensor_func

- Cross Entropy with One Hot Encoding

Pytorch doesn't support Cross Entropy Loss when one hot encoded Tensor is passed. This functionality has been added to tensorop.
```
>> from tensorop.torch_func import cross_ent_onehot
>> y_target = cross_ent_onehot(y_train_onehot)        #y_train_onehot needs to be numpy array, it gives back a FloatLongTensor.
```
Now you can use `nn.CrossEntropyLoss(preds,y_target)` with your preds from model and y_target.


- Using hooks in Pytorch
```
# To add hook, here is the format:
# model.conv.register_forward_hook(get_activation('attr'))
>> get_activation(name) # Usage      #After importing tensorop
# It returns a hook
Note that it only works if forward propagation takes place, so use this function when it has taken place.
```
- Slicing Tensors to get batches
If you've a very large array, it contains images and you want to get fixed batches out of it.
```
for i in x_train.split(t):              # where t denotes elements to keep in first dimension
    preds= model(t)                           
```

- Adding Padding to a Tensor
```
>>> from tensorop.torch_func import add_padding
>>> tensor = add_padding(t,n,c,h,w,pad_value,axis)
```


- Saving and Loading the Model

Saving Checkpoint

```
>> from tensorop.utils import *
>>  save_checkpoint({
        'state_dict':state_dict,
        'epoch':epoch,
    },best,osp.join(PATH,'checkpoint'+str(epoch+1)+'pth.tar'))
# Saves the model in the set PATH
```

Loading the Saved Model

```
>> SAVED_MODEL_PATH = 'dir'
>> model,epoch = load_model(file_name)
```

- Data Augmentation
```
>> from transforms import *
```
- Random2DTranslation
Usage: 
```
tfms_train = tfms.Compose([
    tfms.Random2DTranslation(height,width),
    tfms.RandomHorizontalFlip(),
    tfms.ToTensor(),
    tfms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225]),
])
```

- Effortless conversion between torch Tensors,Numpy array and lists
```
>> from tensorop.torch_func import *
>> torch2np(t)     # Torch Tensor to Numpy
>> np2torch(t)     # Numpy array to Torch Tensor
>> list2torch(t,type)   # List to Torch type(Float/long) Tensor, type can be either 'long' or 'float'
```
- Flattening
```
>> from tensorop.torch_func import *
>> a = torch.tensor([[1,2],[3,4]])  #Example
>> b = np.array([[1,2],[3,4]])
>> a = Flatten(a) # where a is a multi dimensional Torch Tensor
>> b = Flatten(a) # where b is a numpy array
```

------------------------------------------------------------------------------------------------
### np_utils
- Getting categorical vector, normalization of an array
```
>>> from tensorop.np_utils import to_categorical,normalize
>>> to_categorical(y, num_classes)             # Returns Categorical Tensor
>>> normalize(x, axis, order)  # Normalizes a numpy array
```

------------------------------------------------------------------------------------------------
### Optimizers
- To use Cyclic Learning Rate
```
>> from clr import CyclicLR
>> optim = torch.optim.SGD(model.parameters(),lr=lr,momentum=0.9,weight_decay=weight_decay)
>> scheduler = CyclicLR(optim,gamma=gamma,step_size=stepsize)
>> scheduler.batch_step()
```
-------------------------------------------------------------------------------------------------
### Loss Functions
```
>> from loss import cross_entropy,triplet_loss
>> cross_entropy = CrossEntropy(num_classes = num_classes)
>> triplet_loss_fn = TripletLoss(margin=margin)
```

-------------------------------------------------------------------------------------------------

### Kaggle
- When dealing with heavy Pandas dataframes, it is much faster to iterate over `df[col].values` instead of using `df[col].apply` which is a much expensive operation.
For instance: To extract images from a dataframe:
```np.array([strokes2img(x) for x in df['drawing'].values])```

- A multithreaded approach to convert the data to images
``` 
from multiprocessing import Pool
pool = Pool(8)
imgs = pool.map(strokes2img, df[col].values)
```
--------------------------------------------------------------------------------------------------

### Utilities
- Using Logger (Write console output to external text file.)
```
>> from utils import Logger,save_checkpoint
>> sys.stdout = Logger(osp.join(PATH,'log_train.txt'))
```

