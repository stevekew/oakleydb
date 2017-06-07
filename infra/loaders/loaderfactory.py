from oreviewv1 import OReviewLoaderV1

OREVIEWV1_LOADER = 'OReviewV1'


def get_loader(loader_name):

    if loader_name == OREVIEWV1_LOADER:
        loader = OReviewLoaderV1()

    return loader
