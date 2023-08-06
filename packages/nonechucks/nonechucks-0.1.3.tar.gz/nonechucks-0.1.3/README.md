# nonechucks

- [Introduction](#Introduction)
- [Installation](#Installation)
- [Usage](#Usage)
- [Examples](#Examples)
  - [SafeDataset](#SafeDataset)
  - [SafeSampler](#SafeSampler)
- [Contributing](#Contributing)
- [Licensing](#Licensing)

---

<a name="Introduction"></a>

## Introduction
The point of any data processing pipeline is to reduce the burden of doing messy and repetitive tasks for the programmer. PyTorch's flexibly designed data processing module makes it a breeze to do common tasks like shuffling, batching, and iterating through datasets. However, both the dataset and sampler expect you to rid your dataset of any unwanted or corrputed samples before you feed it to them, as they provide no easy way to define what action to take in case an invalid sample is encountered. In fact, for many applications, this defeats the whole point of using a data processing module.

Nonechucks allows you to wrap your existing datasets and samplers

<a name="Installation"></a>

## Installation
To install Nonechucks, simply use pip:

`$ pip install nonechucks`

<a name="Usage"></a>

## Usage

<a name="Example"></a>

## Examples

<a name="SafeDataset"></a>

### SafeDataset

<a name="SafeSampler"></a>

### SafeSampler


<a name="Contributing"></a>

## Contributing

We appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions or extensions, please first open an issue and discuss the feature with us.

<a name="Licensing"></a>

## Licensing

Nonechucks is [MIT licensed](https://github.com/msamogh/nonechucks/blob/master/LICENSE).
