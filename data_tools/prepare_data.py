from AI.src.prepare_data.data_distribute import process_data

local_dir = "/home/yotam/My_Projects/test_cursor/retinanet"

data_root = "/home/yotam/Documents/Projects/cranes/data/labeled_data"
data_config = {
    "name": "feeding",
    "data": [
        {"data_root": data_root + "/feeding_mavic_261221", "train_size": 0.8, "val_size": 0.2},
        {"data_root": data_root + "/feeding_phantom_281221", "train_size": 0.8, "val_size": 0.2},
        {"data_root": data_root + "/feeding_phantom_mosaic_301221", "test_names": ["*"]}
    ],
    "preprocess": [
        {"method": "Blacken", "channel": [2]},
        {"method": "FixFormat"},
        {"method": "Equalize"},
        {"method": "Split", "shape": 448}
    ]
}

project_config = process_data(
    local_dir=local_dir,
    distribute_rule=data_config,
    model='bb'
)


