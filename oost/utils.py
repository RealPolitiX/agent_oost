import numpy as np



def get_random_masks(N, seq_length, n_mask_loc=None):
    '''Generate random binary masks according to specification.
        
        N: int
            Total number of mask instances, each has a length of seq_length.
        seq_length: int
            Length of the sequence to mask.
        n_mask_loc: int
            Number of mask locations.
    '''
    
    if n_mask_loc is None:
        masks = np.random.choice(2, size=(N, seq_length))
    elif n_mask_loc > seq_length:
        raise ValueError("Number of masked locations cannot be more than the total sequence length.")
    else:
        rand_locs = [np.random.choice(seq_length, size=(1, n_mask_loc), replace=False).tolist() for i in range(N)]
        rand_locs = np.array(rand_locs)
        masks = np.zeros((N, seq_length), dtype='int')
        
        for iloc, loc in enumerate(rand_locs):
            masks[iloc, :].put(loc, 1)
    
    return masks