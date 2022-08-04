_base_ = [
    'deepfillv1_base.py', '../default_runtime.py', '../datasets/celeba.py'
]

model = dict(
    train_cfg=dict(disc_step=2, start_iter=0, local_size=(128, 128)), )

input_shape = (256, 256)

train_pipeline = [
    dict(type='LoadImageFromFile', key='gt'),
    dict(
        type='LoadMask',
        mask_mode='bbox',
        mask_config=dict(
            max_bbox_shape=(128, 128),
            max_bbox_delta=40,
            min_margin=20,
            img_shape=input_shape)),
    dict(
        type='Crop',
        keys=['gt'],
        crop_size=(384, 384),
        random_crop=True,
    ),
    dict(
        type='Resize',
        keys=['gt'],
        scale=input_shape,
        keep_ratio=False,
    ),
    dict(type='GetMaskedImage'),
    dict(type='PackEditInputs'),
]

test_pipeline = train_pipeline

train_dataloader = dict(
    batch_size=16,
    sampler=dict(shuffle=False),
    dataset=dict(pipeline=train_pipeline),
)

val_dataloader = dict(
    batch_size=1,
    dataset=dict(pipeline=test_pipeline),
)

test_dataloader = val_dataloader

train_cfg = dict(
    type='IterBasedTrainLoop',
    max_iters=1500003,
    val_interval=250000,
)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

lr_config = dict(policy='Fixed', by_epoch=False)

checkpoint = dict(type='CheckpointHook', interval=250000, by_epoch=False)