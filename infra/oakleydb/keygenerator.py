class KeyGenerator(object):

    @staticmethod
    def get_lens_key(lens_details):
        return "{}_{}".format(lens_details['name'], lens_details['lenstype'])
