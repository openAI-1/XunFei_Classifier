 
__all__ = ['resnet18','resnet34', 'resnet50','resnest18','resnest50','efficientnet-b5'\
            'efficientnet-b7','efficientnet-b3','bilinearnet_b5','finenet50','directnet50','densenet121','densenet169','simple_net','vgg16','res2net50','res2net18','res2next50', \
            'res2next18','se_resnet18', 'se_resnet10', ]


data_config = {
    'Adver_Material':'./converter/csv_file/adver_material.csv',
    'Crop_Growth':'./converter/csv_file/crop_growth_post.csv',
    'Photo_Guide':'./converter/csv_file/photo_guide_merge_fake.csv', #photo_guide_merge.csv
    'Leve_Disease':'./converter/csv_file/leve_disease.csv',#processed_leve_disease.csv
    'Temp_Freq':'./converter/csv_file/temp_freq.csv',
    'Farmer_Work':'./converter/csv_file/farmer_work_final_v3.csv', #farmer_work_lite_external_v3.csv
    'Covid19':'./converter/csv_file/covid19.csv',
    'Family_Env':'./converter/csv_file/family_env.csv',
}

num_classes = {
    'Adver_Material':137,
    'Crop_Growth':4,
    'Photo_Guide':8,
    'Leve_Disease':3,
    'Temp_Freq':24,
    'Farmer_Work':4,
    'Covid19':2,
    'Family_Env':6
}

TASK = 'Photo_Guide'
NET_NAME = 'efficientnet-b5'
VERSION = 'v6.0-pretrained-fake' #v6.0-pretrained-new
DEVICE = '3'
# Must be True when pre-training and inference
PRE_TRAINED = True
# 1,2,3,4
CURRENT_FOLD = 2
GPU_NUM = len(DEVICE.split(','))
FOLD_NUM = 5
TTA_TIMES = 5


NUM_CLASSES = num_classes[TASK]
from utils import get_weight_path,get_weight_list

CSV_PATH = data_config[TASK]
CKPT_PATH = './ckpt/{}/{}/fold{}'.format(TASK,VERSION,str(CURRENT_FOLD))
# CKPT_PATH = './ckpt/{}/{}/fold{}'.format(TASK,'v6.0-pretrained',str(CURRENT_FOLD))
WEIGHT_PATH = get_weight_path(CKPT_PATH)
print(WEIGHT_PATH)

if PRE_TRAINED:
    WEIGHT_PATH_LIST = get_weight_list('./ckpt/{}/{}/'.format(TASK,VERSION))
else:
    WEIGHT_PATH_LIST = None

# WEIGHT_PATH_LIST = None

MEAN = {
    'Adver_Material':[0.485, 0.456, 0.406], 
    'Crop_Growth':None,
    'Photo_Guide':(0.450),
    'Leve_Disease':(0.496,0.527,0.387),
    'Temp_Freq':None,
    'Farmer_Work':(0.486,0.496,0.403), #(0.486,0.496,0.403) (0.479)
    'Covid19':None,
    'Family_Env':None
}

STD = {
    'Adver_Material':[0.229, 0.224, 0.225],
    'Crop_Growth':None,
    'Photo_Guide':(0.224),
    'Leve_Disease':(0.230,0.216,0.237),
    'Temp_Freq':None,
    'Farmer_Work':(0.237,0.231,0.246), #(0.237,0.231,0.246) (0.228)
    'Covid19':None,
    'Family_Env':None
    
}

MILESTONES = {
    'Adver_Material':[30,60,90],
    'Crop_Growth':[30,60,90],
    'Photo_Guide':[30,60,90],
    'Leve_Disease':[30,60,90],
    'Temp_Freq':[30,60,90],
    'Farmer_Work':[30,60,90],
    'Covid19':[30,60,90],
    'Family_Env':[30,60,90]
}

EPOCH = {
    'Adver_Material':150,
    'Crop_Growth':120,
    'Photo_Guide':120, #120
    'Leve_Disease':120,
    'Temp_Freq':120,
    'Farmer_Work':50,
    'Covid19':120,
    'Family_Env':120
}

TRANSFORM = {
    'Adver_Material':[2,6,7,8,9],#[6,7,8,2,9]
    'Crop_Growth':[18,6,7,8,13,9,19],
    'Photo_Guide':[18,2,6,9,19],#[18,2,6,9,19] v5.2 v6.0-pretrained v6.0-all-pre,v6.0-pre-new,v6.0-pre-fake
    'Leve_Disease':[2,18,6,7,8,9,19], #[2,6,7,8,9,10,19] (6.2-pre) (7,8-p=1) / [2,18,6,7,8,9,19](6.0-pre-new)
    'Temp_Freq':[2,4,9,19], #[2,3,4,9,19](6.0-pre) [2,4,9,19](6.1-pre) 
    'Farmer_Work':[2,6,7,8,9,10,19], #v6.0-pre v6.0-crop-pre (7,8-p=1)
    'Covid19':[2,18,6,7,8,9,19],
    'Family_Env':[20,2,4,7,8,9,19] #[2,4,9,19] v6.0-pre  [20,2,4,7,8,9,19] v6.0-pre-new 
}

SHAPE = {
    'Adver_Material':(512, 512),
    'Crop_Growth':(256, 256),
    'Photo_Guide':(256, 256),
    'Leve_Disease':(512, 512),
    'Temp_Freq':(512,512),
    'Farmer_Work':(512,512),
    'Covid19':(256, 256),
    'Family_Env':(512,512)
}


CHANNEL = {
    'Adver_Material':3,
    'Crop_Growth':3,
    'Photo_Guide':3,# C=1 v5.2 v6.0-pretrained /C=3 v6.0-all-pre,v6.0-pre-new,v6.0-pre-fake
    'Leve_Disease':3,
    'Temp_Freq':3,
    'Farmer_Work':3, #3
    'Covid19':3,
    'Family_Env':3
}

# Arguments when trainer initial
INIT_TRAINER = {
    'net_name': NET_NAME,
    'lr': 1e-3 if not PRE_TRAINED else 5e-4, #1e-3
    'n_epoch': EPOCH[TASK],
    'channels': CHANNEL[TASK],
    'num_classes': NUM_CLASSES,
    'input_shape': SHAPE[TASK],
    'crop': 0,
    'batch_size': 32,
    'num_workers': 2,
    'device': DEVICE,
    'pre_trained': PRE_TRAINED,
    'weight_path': WEIGHT_PATH,
    'weight_decay': 0.0001, #0.0001
    'momentum': 0.9,
    'mean': MEAN[TASK],
    'std': STD[TASK],
    'gamma': 0.1,
    'milestones': MILESTONES[TASK],
    'use_fp16':True,
    'transform':TRANSFORM[TASK],
    'drop_rate': 0.5, #0.5
    'smothing':0.15,
    'external_pretrained':True if 'pretrained' in VERSION else False,#False
}

# no_crop     

# mean:0.131
# std:0.209

#crop
# mean:0.189
# std:0.185


# Arguments when perform the trainer
__loss__ = ['Cross_Entropy','TopkCrossEntropy','SoftCrossEntropy','F1_Loss','TopkSoftCrossEntropy','DynamicTopkCrossEntropy','DynamicTopkSoftCrossEntropy']
LOSS_FUN = 'Cross_Entropy'
# Arguments when perform the trainer

CLASS_WEIGHT = {
    'Adver_Material':None,
    'Crop_Growth':None,
    'Photo_Guide':None,
    'Leve_Disease':None,
    'Temp_Freq':None,
    'Farmer_Work':None,
    'Covid19':[1.0,2.0],
    'Family_Env':None
}


MONITOR = {
    'Adver_Material':'val_acc', 
    'Crop_Growth':'val_acc',
    'Photo_Guide':'val_acc',
    'Leve_Disease':'val_acc',
    'Temp_Freq':'val_acc',
    'Farmer_Work':'val_acc', 
    'Covid19':'val_f1',
    'Family_Env':'val_acc'
}

SETUP_TRAINER = {
    'output_dir': './ckpt/{}/{}'.format(TASK,VERSION),
    'log_dir': './log/{}/{}'.format(TASK,VERSION),
    'optimizer': 'Adam',
    'loss_fun': LOSS_FUN,
    'class_weight': CLASS_WEIGHT[TASK],
    'lr_scheduler': 'MultiStepLR', #'MultiStepLR'
    'balance_sample':True if 'balance' in VERSION else False,#False
    'monitor':MONITOR[TASK]
}
