# PUJetId_training_plotting

## Training
-----------
1. Make input `TTrees` for `BDT` training with `TMVA`.

    either you can make it interactively
    ```bash
    cd training/input
    ./run_make_trees.sh
    ```
    
    or submit to condor.
    ```bash
    cd training/input
    condor_submit submit_make_trees.sub
    ```
    
    **Note**: This will work on `lxplus`, make appropriate changes in python script to make it work.
    
2. Training
    
    `train_bdt.py` is the main training script.
    `--max_N` is the number of entries to use for training set and testing set, i.e. `max_N / 2` number of entries will be used for `train_signal`, `train_background`, `test_signal` and `test_background`. In case the `TTrees` for `signal` or `background` has less number of entries than `max_N`, then that number will be used.
    
    running the training interactively, the argument is `eta_bin`, open `run_train_bdt.sh` and change the `in_dir`.
    ```bash
    cd training
    ./run_train_bdt.sh Eta0p0To2p5
    ```
    or submit condor jobs
    ```bash
    cd training
    condor_submit submit_train_bdt.sub
    ```