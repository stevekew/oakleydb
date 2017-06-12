class KeyGenerator(object):

    @staticmethod
    def get_lens_key(lens_details):
        return "{}_{}".format(lens_details['name'], lens_details['lenstype'])

    @staticmethod
    def get_model_key(model_details):
        return "{}_{}_{}".format(model_details['style'], model_details['name'], model_details['sku'])
