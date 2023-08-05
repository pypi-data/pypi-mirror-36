# NIPS Adversarial Vision Challenge

[![Build Status](https://travis-ci.org/bethgelab/adversarial-vision-challenge.svg?branch=master)](https://travis-ci.org/bethgelab/adversarial-vision-challenge)

### Publication

https://arxiv.org/abs/1808.01976

### Installation

To install the package simply run:

`pip install adversarial-vision-challenge`

This package contains helper functions to implement models and attacks that can be used with Python 2.7, 3.4, 3.5 and 3.6. Other Python versions might work as well. **We recommend using Python 3**!

Furthermore, this package also contains test scripts that should be used before submission to perform local tests of your model or attack. These test scripts are Python 3 only, because they depend on `crowdai-repo2docker`. See `Running Tests Scripts` section below for more detailed information.


### Implementing a model

To run a model server, load your model and wrap it as a [foolbox model](https://foolbox.readthedocs.io/en/latest/modules/models.html).
Then pass the foolbox model to the `model_server` function.

```python
from adversarial_vision_challenge import model_server

foolbox_model = load_your_foolbox_model()
model_server(foolbox_model)
```

### Implementing an attack

To run an attack, use the `load_model` method to get a model instance that is callable to get the predicted labels.

```python
from adversarial_vision_challenge.utils import read_images, store_adversarial
from adversarial_vision_challenge.utils import load_model

model = load_model()

for (file_name, image, label) in read_images():
    # model is callable and returns the predicted class,
    # i.e. 0 <= model(image) < 200

    # run your adversarial attack
    adversarial = your_attack(model, image, label)

    # store the adversarial
    store_adversarial(file_name, adversarial)
    
 ### Running the tests scripts
```

### Running Tests Scripts

The test scripts (running on your host machine) will need Python 3. Your model or attack running inside a docker container and using this package can use Python 2 or 3.

- To test a model, run the following: `avc-test-model .`
- To test an untargeted attack, run the following: `avc-test-untargeted-attack .`
- To test an targeted attack, run the following: `avc-test-targeted-attack .`

within the folders you want to test.

In order for the attacks to work, your models / attack folders need to have the following structure:
- for models: https://gitlab.crowdai.org/adversarial-vision-challenge/nips18-avc-model-template
- for attacks: https://gitlab.crowdai.org/adversarial-vision-challenge/nips18-avc-attack-template


## FAQ

#### Can you recommend some papers to get more familiar with adversarial examples, attacks and the threat model considered in this NIPS competition?
Have a look at our [reading list](https://medium.com/@wielandbr/reading-list-for-the-nips-2018-adversarial-vision-challenge-63cbac345b2f) that summarizes papers relevant for this competition.

#### How can I cite the competition in my own work?
```
@inproceedings{adversarial_vision_challenge,
title = {Adversarial Vision Challenge},
author = {Brendel, Wieland and Rauber, Jonas and Kurakin, Alexey and Papernot, Nicolas and Veliqi, Behar and Salath{\'e}, Marcel and Mohanty, Sharada P and Bethge, Matthias},
booktitle = {32nd Conference on Neural Information Processing Systems (NIPS 2018) Competition Track},
year = {2018},
url = {https://arxiv.org/abs/1808.01976}
}
```

#### Why can I not pass bounds = (0, 1) when creating the foolbox model?
We expect that all models process images that have values between 0 and 255. Therefore, we enforce that the model bounds are set to (0, 255). If your model expects images with values between 0 and 1, you can just pass `bounds=(0, 255)` and `preprocessing=(0, 255)`, then the Foolbox model wrapper will divide all inputs by 255. Alternatively, you can leave preprocessing at `(0, 1)` and change your model to expect values between 0 and 255.


#### How is the score for an individual model, attack, image calculated?
We normalize the pixel values of the clean image and the adversarial to be between 0 and 1 and then take the L2 norm of the perturbation (adverarial - clean) as if they were vectors.
