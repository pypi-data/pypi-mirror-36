#!/usr/bin/env python3
"""
Batching procedures
===================

Iterators implementing common batching strategies.
"""

import numpy as np


class NumpyBatchIterator(object):
    """Wraps a list of numpy arrays and a list of targets as a batch iterator.

    You can then iterate over this object and get tuples of
    ``batch_data, batch_targets`` ready for use in your computation graph.

    Example for classification:

    .. code-block:: python

        # 1000 10-dimensional inputs
        data = np.random.uniform(size=(1000, 10))
        # Class labels
        labels = np.random.randint(10, size=1000)
        # Iterator
        batched_dataset = NumpyBatchIterator(data, labels, batch_size=20)
        # Training loop
        for x, y in batched_dataset:
            # x has shape (10, 20) while y has shape (20,)
            # Do something with x and y


    Example for multidimensional regression:

    .. code-block:: python

        # 1000 10-dimensional inputs
        data = np.random.uniform(size=(1000, 10))
        # 5-dimensional outputs
        labels = np.random.uniform(size=(1000, 5))
        # Iterator
        batched_dataset = NumpyBatchIterator(data, labels, batch_size=20)
        # Training loop
        for x, y in batched_dataset:
            # x has shape (10, 20) while y has shape (5, 20)
            # Do something with x and y


    Args:
        data (list): List of numpy arrays containing the data
        targets (list): List of targets
        batch_size (int, optional): Batch size (default: ``32``)
        shuffle (bool, optional): Shuffle the dataset whenever starting a new
            iteration (default: ``True``)
    """

    def __init__(
        self,
        data,
        targets,
        batch_size=32,
        shuffle=True,
    ):

        if len(data) != len(targets):
            raise ValueError(
                f"Data and targets size mismatch ({len(data)} "
                f"vs {len(targets)})"
            )

        # The data is stored as a fortran contiguous array so having the
        # batch size last is faster
        self.data = np.asfortranarray(
            np.stack([np.atleast_1d(sample) for sample in data], axis=-1)
        )
        self.targets = np.asfortranarray(
            np.stack([target for target in targets], axis=-1)
        )

        self.batch_size = batch_size
        self.shuffle = shuffle
        self.length = len(self.targets)
        self.position = 0
        self.indices = np.arange(self.length)

        self.reset()

    def __len__(self):
        """This returns the number of **batches** in the dataset
        (not the total number of samples)

        Returns:
            int: Number of batches in the dataset
                ``ceil(len(data)/batch_size)``
        """
        return int(np.ceil(self.length / self.batch_size))

    def __getitem__(self, index):
        """Returns the ``index``th **batch** (not sample)

        This returns something different every time the data is shuffled.

        The result is a tuple ``batch_data, batch_target`` where each of those
        is a numpy array in Fortran layout (for more efficient input in dynet).
        The batch size is always the last dimension.

        Args:
            index (int, slice): Index or slice

        Returns:
            tuple: ``batch_data, batch_target``
        """
        batch_data = self.data[..., index]
        batch_targets = self.targets[..., index]
        return batch_data, batch_targets

    def percentage_done(self):
        """What percent of the data has been covered in the current epoch"""
        return 100 * (self.position / self.length)

    def just_passed_multiple(self, batch_number):
        """Checks whether the current number of batches processed has
        just passed a multiple of ``batch_number``.

        For example you can use this to report at regular interval
        (eg. every 10 batches)

        Args:
            batch_number (int): [description]

        Returns:
            bool: ``True`` if :math:`\\fraccurrent_batch`
        """
        batch_position = self.position // self.batch_size
        return batch_position % batch_number == 0

    def reset(self):
        """Reset the iterator and shuffle the dataset if applicable"""
        self.position = 0
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __iter__(self):
        self.reset()
        return self

    def __next__(self):
        # Check for end of epoch
        if self.position > self.length:
            raise StopIteration
        # Retrieve random indices for the batch
        start_idx = self.position
        stop_idx = min(self.position + self.batch_size, self.length-1)
        idx_range = self.indices[start_idx:stop_idx]
        # Increment position
        self.position += self.batch_size
        # Return batch
        return self[idx_range]
